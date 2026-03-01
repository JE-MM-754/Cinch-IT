"""
Outreach service — handles email, SMS, and voice outreach.
ALL outreach respects the TEST_MODE safety gate.
"""

import json
from datetime import datetime, timezone
from typing import Optional
from sqlalchemy.orm import Session

from config import get_settings
from models import Contact, OutreachEvent, AuditLog

settings = get_settings()


class OutreachSafetyError(Exception):
    """Raised when outreach would violate safety rules."""
    pass


def _enforce_safety(contact: Contact, channel: str):
    """
    NON-NEGOTIABLE safety checks before any outreach.
    Raises OutreachSafetyError if outreach should not proceed.
    """
    # 1. Test mode: only send to test contact
    if settings.test_mode:
        if channel == "email" and contact.email != settings.test_contact_email.lower():
            raise OutreachSafetyError(
                f"TEST_MODE is ON. Cannot send {channel} to {contact.email}. "
                f"Only {settings.test_contact_email} is allowed."
            )
        if channel in ("sms", "voice"):
            test_phone = settings.test_contact_phone
            if contact.phone != test_phone and contact.mobile != test_phone:
                raise OutreachSafetyError(
                    f"TEST_MODE is ON. Cannot send {channel} to {contact.phone}. "
                    f"Only {settings.test_contact_phone} is allowed."
                )

    # 2. Do not contact
    if contact.do_not_contact:
        raise OutreachSafetyError(
            f"Contact {contact.id} ({contact.first_name} {contact.last_name}) "
            f"is marked DO NOT CONTACT. Reason: {contact.do_not_contact_reason}"
        )

    # 3. Channel consent
    if channel == "sms" and not contact.sms_consent:
        raise OutreachSafetyError(
            f"Contact {contact.id} has not given SMS consent. "
            "SMS requires prior express consent (TCPA)."
        )
    if channel == "voice" and not contact.voice_consent:
        raise OutreachSafetyError(
            f"Contact {contact.id} has not given voice consent. "
            "AI voice calls require prior express written consent (TCPA)."
        )

    # 4. Required contact info
    if channel == "email" and not contact.email:
        raise OutreachSafetyError(f"Contact {contact.id} has no email address.")
    if channel == "sms" and not (contact.mobile or contact.phone):
        raise OutreachSafetyError(f"Contact {contact.id} has no phone number for SMS.")
    if channel == "voice" and not (contact.phone or contact.mobile):
        raise OutreachSafetyError(f"Contact {contact.id} has no phone number for voice.")


def _log_audit(db: Session, action: str, entity_type: str, entity_id: int, details: dict):
    """Write to audit log."""
    log = AuditLog(
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        details=json.dumps(details),
        user="system"
    )
    db.add(log)


def send_email(db: Session, contact: Contact, subject: str, body: str,
               sequence_step: int = 1, template_id: str = "") -> OutreachEvent:
    """
    Send an email to a contact. Respects all safety gates.
    Returns the OutreachEvent record.
    """
    _enforce_safety(contact, "email")

    event = OutreachEvent(
        contact_id=contact.id,
        channel="email",
        status="queued",
        sequence_step=sequence_step,
        subject=subject,
        body=body,
        template_id=template_id,
        is_test=settings.test_mode,
    )
    db.add(event)
    db.flush()

    # Actually send via SendGrid
    if settings.sendgrid_api_key:
        try:
            from sendgrid import SendGridAPIClient
            from sendgrid.helpers.mail import Mail, TrackingSettings, OpenTracking, ClickTracking

            target_email = settings.test_contact_email if settings.test_mode else contact.email

            message = Mail(
                from_email=(settings.sendgrid_from_email, settings.sendgrid_from_name),
                to_emails=target_email,
                subject=subject,
                html_content=body,
            )

            # Enable open and click tracking
            tracking = TrackingSettings()
            tracking.open_tracking = OpenTracking(True)
            tracking.click_tracking = ClickTracking(True, True)
            message.tracking_settings = tracking

            # Add unsubscribe header (CAN-SPAM)
            # TODO: Set up proper unsubscribe link once domain is live

            sg = SendGridAPIClient(settings.sendgrid_api_key)
            response = sg.send(message)

            event.status = "sent"
            event.sent_at = datetime.now(timezone.utc)
            event.provider_message_id = response.headers.get('X-Message-Id', '')

        except Exception as e:
            event.status = "failed"
            event.notes = str(e)
    else:
        # No API key — log as queued (dev mode)
        event.status = "queued"

    # Update contact
    contact.last_outreach_at = datetime.now(timezone.utc)
    contact.current_sequence_step = sequence_step

    # Audit
    _log_audit(db, "email_sent" if event.status == "sent" else "email_queued",
               "outreach_event", event.id, {
                   "contact_id": contact.id,
                   "channel": "email",
                   "subject": subject,
                   "status": event.status,
                   "is_test": settings.test_mode,
                   "target_email": settings.test_contact_email if settings.test_mode else contact.email,
               })

    return event


def send_sms(db: Session, contact: Contact, body: str,
             sequence_step: int = 1) -> OutreachEvent:
    """
    Send an SMS to a contact. Requires SMS consent.
    """
    _enforce_safety(contact, "sms")

    event = OutreachEvent(
        contact_id=contact.id,
        channel="sms",
        status="queued",
        sequence_step=sequence_step,
        body=body,
        is_test=settings.test_mode,
    )
    db.add(event)
    db.flush()

    if settings.twilio_account_sid and settings.twilio_auth_token:
        try:
            from twilio.rest import Client

            client = Client(settings.twilio_account_sid, settings.twilio_auth_token)
            target_phone = settings.test_contact_phone if settings.test_mode else (contact.mobile or contact.phone)

            # Append opt-out instruction (TCPA compliance)
            sms_body = f"{body}\n\nReply STOP to opt out."

            message = client.messages.create(
                body=sms_body,
                from_=settings.twilio_phone_number,
                to=target_phone,
            )

            event.status = "sent"
            event.sent_at = datetime.now(timezone.utc)
            event.provider_message_id = message.sid

        except Exception as e:
            event.status = "failed"
            event.notes = str(e)
    else:
        event.status = "queued"

    contact.last_outreach_at = datetime.now(timezone.utc)

    _log_audit(db, "sms_sent" if event.status == "sent" else "sms_queued",
               "outreach_event", event.id, {
                   "contact_id": contact.id,
                   "channel": "sms",
                   "status": event.status,
                   "is_test": settings.test_mode,
               })

    return event


def send_voice(db: Session, contact: Contact, script: str,
               sequence_step: int = 1) -> OutreachEvent:
    """
    Initiate an AI voice call. Requires voice consent.
    """
    _enforce_safety(contact, "voice")

    event = OutreachEvent(
        contact_id=contact.id,
        channel="voice",
        status="queued",
        sequence_step=sequence_step,
        body=script,
        is_test=settings.test_mode,
    )
    db.add(event)
    db.flush()

    # TODO: Implement Bland.ai or Twilio voice integration
    # For now, just queue it
    event.status = "queued"

    _log_audit(db, "voice_queued", "outreach_event", event.id, {
        "contact_id": contact.id,
        "channel": "voice",
        "status": event.status,
        "is_test": settings.test_mode,
    })

    return event
