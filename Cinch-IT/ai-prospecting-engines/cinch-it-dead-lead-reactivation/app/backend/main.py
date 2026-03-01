"""
Dead Lead Reactivation API — FastAPI Application
Cinch IT Boston
"""

from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional
from datetime import datetime, timezone
import json
import os

from config import get_settings
from database import get_db, init_database
from models import Contact, OutreachEvent, Meeting, EmailSequence, SequenceStep, AuditLog
from services.outreach import send_email, send_sms, OutreachSafetyError
from services.response_classifier import classify_response
from services.sequences import create_sms_first_sequences, get_best_sequence_for_contact

settings = get_settings()

app = FastAPI(
    title="Cinch IT Dead Lead Reactivation",
    version="0.1.0",
    description="AI-powered dead lead reactivation system for Cinch IT Boston",
)

# CORS — lock down in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url] if settings.app_env == "production" else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    init_database()


# ──────────────────────────────────────────────
# Health & Status
# ──────────────────────────────────────────────

@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "test_mode": settings.test_mode,
        "env": settings.app_env,
        "version": "0.1.0",
    }


@app.get("/api/dashboard/stats")
def dashboard_stats(db: Session = Depends(get_db)):
    """Main dashboard statistics with SMS-first focus."""
    total_contacts = db.query(func.count(Contact.id)).scalar()
    ready = db.query(func.count(Contact.id)).filter(Contact.status == "ready").scalar()
    needs_enrichment = db.query(func.count(Contact.id)).filter(Contact.status == "needs_enrichment").scalar()
    do_not_contact = db.query(func.count(Contact.id)).filter(Contact.do_not_contact == True).scalar()
    enriched = db.query(func.count(Contact.id)).filter(Contact.apollo_enriched == True).scalar()
    
    # SMS-first metrics
    sms_ready = db.query(func.count(Contact.id)).filter(
        Contact.sms_consent == True, 
        (Contact.phone != "") | (Contact.mobile != "")
    ).scalar()
    email_only = db.query(func.count(Contact.id)).filter(
        Contact.sms_consent == False,
        Contact.email != ""
    ).scalar()

    total_outreach = db.query(func.count(OutreachEvent.id)).scalar()
    
    # SMS metrics
    sms_sent = db.query(func.count(OutreachEvent.id)).filter(
        OutreachEvent.channel == "sms", OutreachEvent.status == "sent"
    ).scalar()
    sms_replies = db.query(func.count(OutreachEvent.id)).filter(
        OutreachEvent.channel == "sms", OutreachEvent.replied_at.isnot(None)
    ).scalar()
    
    # Email metrics  
    emails_sent = db.query(func.count(OutreachEvent.id)).filter(
        OutreachEvent.channel == "email", OutreachEvent.status == "sent"
    ).scalar()
    emails_opened = db.query(func.count(OutreachEvent.id)).filter(
        OutreachEvent.channel == "email", OutreachEvent.opened_at.isnot(None)
    ).scalar()
    email_replies = db.query(func.count(OutreachEvent.id)).filter(
        OutreachEvent.channel == "email", OutreachEvent.replied_at.isnot(None)
    ).scalar()
    
    total_replies = sms_replies + email_replies
    meetings_booked = db.query(func.count(Meeting.id)).scalar()

    return {
        "contacts": {
            "total": total_contacts,
            "ready": ready,
            "needs_enrichment": needs_enrichment,
            "do_not_contact": do_not_contact,
            "enriched": enriched,
            "sms_ready": sms_ready,
            "email_only": email_only,
        },
        "outreach": {
            "total": total_outreach,
            "sms_sent": sms_sent,
            "sms_replies": sms_replies,
            "sms_reply_rate": round(sms_replies / sms_sent * 100, 1) if sms_sent > 0 else 0,
            "emails_sent": emails_sent,
            "emails_opened": emails_opened,
            "email_open_rate": round(emails_opened / emails_sent * 100, 1) if emails_sent > 0 else 0,
            "email_replies": email_replies,
            "email_reply_rate": round(email_replies / emails_sent * 100, 1) if emails_sent > 0 else 0,
            "total_replies": total_replies,
            "overall_reply_rate": round(total_replies / (sms_sent + emails_sent) * 100, 1) if (sms_sent + emails_sent) > 0 else 0,
            "meetings_booked": meetings_booked,
        },
        "test_mode": settings.test_mode,
        "strategy": "sms_first",
    }


# ──────────────────────────────────────────────
# Contacts
# ──────────────────────────────────────────────

@app.get("/api/contacts")
def list_contacts(
    status: Optional[str] = None,
    search: Optional[str] = None,
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    """List contacts with optional filters."""
    query = db.query(Contact)

    if status:
        query = query.filter(Contact.status == status)
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (Contact.first_name.ilike(search_term)) |
            (Contact.last_name.ilike(search_term)) |
            (Contact.company.ilike(search_term)) |
            (Contact.email.ilike(search_term))
        )

    total = query.count()
    contacts = query.order_by(Contact.last_activity.desc()).offset(
        (page - 1) * per_page
    ).limit(per_page).all()

    return {
        "contacts": [
            {
                "id": c.id,
                "first_name": c.first_name,
                "last_name": c.last_name,
                "company": c.company,
                "email": c.email,
                "phone": c.phone,
                "mobile": c.mobile,
                "last_activity": c.last_activity,
                "status": c.status,
                "do_not_contact": c.do_not_contact,
                "apollo_enriched": c.apollo_enriched,
                "business_verified": c.business_verified,
                "current_sequence_step": c.current_sequence_step,
                "last_outreach_at": c.last_outreach_at.isoformat() if c.last_outreach_at else None,
                "sms_consent": c.sms_consent,
                "voice_consent": c.voice_consent,
            }
            for c in contacts
        ],
        "total": total,
        "page": page,
        "per_page": per_page,
        "pages": (total + per_page - 1) // per_page,
    }


@app.get("/api/contacts/{contact_id}")
def get_contact(contact_id: int, db: Session = Depends(get_db)):
    """Get detailed contact info including outreach history."""
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")

    events = db.query(OutreachEvent).filter(
        OutreachEvent.contact_id == contact_id
    ).order_by(OutreachEvent.created_at.desc()).all()

    meetings = db.query(Meeting).filter(
        Meeting.contact_id == contact_id
    ).order_by(Meeting.scheduled_at.desc()).all()

    enrichment = json.loads(contact.enrichment_data) if contact.enrichment_data else {}

    return {
        "contact": {
            "id": contact.id,
            "first_name": contact.first_name,
            "last_name": contact.last_name,
            "company": contact.company,
            "email": contact.email,
            "phone": contact.phone,
            "mobile": contact.mobile,
            "last_activity": contact.last_activity,
            "status": contact.status,
            "do_not_contact": contact.do_not_contact,
            "do_not_contact_reason": contact.do_not_contact_reason,
            "apollo_enriched": contact.apollo_enriched,
            "business_verified": contact.business_verified,
            "business_active": contact.business_active,
            "enrichment": enrichment,
            "email_consent": contact.email_consent,
            "sms_consent": contact.sms_consent,
            "voice_consent": contact.voice_consent,
            "current_sequence_step": contact.current_sequence_step,
            "notes": contact.notes,
        },
        "outreach_history": [
            {
                "id": e.id,
                "channel": e.channel,
                "status": e.status,
                "subject": e.subject,
                "sequence_step": e.sequence_step,
                "sent_at": e.sent_at.isoformat() if e.sent_at else None,
                "opened_at": e.opened_at.isoformat() if e.opened_at else None,
                "replied_at": e.replied_at.isoformat() if e.replied_at else None,
                "response_type": e.response_type,
                "is_test": e.is_test,
            }
            for e in events
        ],
        "meetings": [
            {
                "id": m.id,
                "scheduled_at": m.scheduled_at.isoformat(),
                "status": m.status,
                "assigned_to": m.assigned_to,
                "notes": m.notes,
            }
            for m in meetings
        ],
    }


@app.patch("/api/contacts/{contact_id}")
def update_contact(contact_id: int, updates: dict, db: Session = Depends(get_db)):
    """Update contact fields."""
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")

    allowed_fields = {
        "do_not_contact", "do_not_contact_reason", "notes",
        "sms_consent", "voice_consent", "status"
    }

    for field, value in updates.items():
        if field in allowed_fields:
            setattr(contact, field, value)

    # If marked DNC, update status
    if updates.get("do_not_contact"):
        contact.status = "do_not_contact"

    db.commit()

    audit = AuditLog(
        action="contact_updated",
        entity_type="contact",
        entity_id=contact_id,
        details=json.dumps({"fields_updated": list(updates.keys())}),
    )
    db.add(audit)
    db.commit()

    return {"status": "updated", "contact_id": contact_id}


# ──────────────────────────────────────────────
# Outreach
# ──────────────────────────────────────────────

@app.post("/api/outreach/send-test-email")
def send_test_email_endpoint(
    subject: str = "Test Email from Cinch IT Reactivation System",
    body: str = "<p>This is a test email. If you received this, the system is working.</p>",
    db: Session = Depends(get_db),
):
    """Send a test email to Jamie's test address. Only works in test mode."""
    if not settings.test_mode:
        raise HTTPException(status_code=403, detail="Test endpoint only available in test mode")

    # Create or get test contact
    test_contact = db.query(Contact).filter(Contact.email == settings.test_contact_email.lower()).first()
    if not test_contact:
        test_contact = Contact(
            first_name="Jamie",
            last_name="Erickson",
            company="Test",
            email=settings.test_contact_email.lower(),
            phone=settings.test_contact_phone,
            status="ready",
            email_consent=True,
        )
        db.add(test_contact)
        db.flush()

    try:
        event = send_email(db, test_contact, subject, body)
        db.commit()
        return {
            "status": "sent" if event.status == "sent" else "queued",
            "event_id": event.id,
            "message": f"Test email {'sent' if event.status == 'sent' else 'queued'} to {settings.test_contact_email}",
        }
    except OutreachSafetyError as e:
        raise HTTPException(status_code=403, detail=str(e))


@app.post("/api/outreach/send-email/{contact_id}")
def send_email_endpoint(
    contact_id: int,
    payload: dict,
    db: Session = Depends(get_db),
):
    """Send an email to a specific contact."""
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")

    subject = payload.get("subject", "")
    body = payload.get("body", "")
    sequence_step = payload.get("sequence_step", 1)

    if not subject or not body:
        raise HTTPException(status_code=400, detail="Subject and body are required")

    try:
        event = send_email(db, contact, subject, body, sequence_step)
        db.commit()
        return {"status": event.status, "event_id": event.id}
    except OutreachSafetyError as e:
        raise HTTPException(status_code=403, detail=str(e))


@app.post("/api/outreach/send-sms/{contact_id}")
def send_sms_endpoint(
    contact_id: int,
    payload: dict,
    db: Session = Depends(get_db),
):
    """Send an SMS to a specific contact."""
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")

    body = payload.get("body", "")
    sequence_step = payload.get("sequence_step", 1)

    if not body:
        raise HTTPException(status_code=400, detail="Message body is required")

    try:
        event = send_sms(db, contact, body, sequence_step)
        db.commit()
        return {"status": event.status, "event_id": event.id}
    except OutreachSafetyError as e:
        raise HTTPException(status_code=403, detail=str(e))


@app.post("/api/outreach/send-test-sms")
def send_test_sms_endpoint(
    body: str = "Test SMS from Cinch IT Reactivation System. If you received this, SMS is working!",
    db: Session = Depends(get_db),
):
    """Send a test SMS to Jamie's test number. Only works in test mode."""
    if not settings.test_mode:
        raise HTTPException(status_code=403, detail="Test endpoint only available in test mode")

    # Create or get test contact
    test_contact = db.query(Contact).filter(Contact.phone == settings.test_contact_phone).first()
    if not test_contact:
        test_contact = Contact(
            first_name="Jamie",
            last_name="Erickson", 
            company="Test",
            email=settings.test_contact_email.lower(),
            phone=settings.test_contact_phone,
            status="ready",
            sms_consent=True,
            email_consent=True,
        )
        db.add(test_contact)
        db.flush()

    try:
        event = send_sms(db, test_contact, body)
        db.commit()
        return {
            "status": "sent" if event.status == "sent" else "queued",
            "event_id": event.id,
            "message": f"Test SMS {'sent' if event.status == 'sent' else 'queued'} to {settings.test_contact_phone}",
        }
    except OutreachSafetyError as e:
        raise HTTPException(status_code=403, detail=str(e))


@app.post("/api/outreach/classify-response")
def classify_response_endpoint(payload: dict):
    """Classify an inbound reply using AI."""
    reply_text = payload.get("reply_text", "")
    if not reply_text:
        raise HTTPException(status_code=400, detail="reply_text is required")

    result = classify_response(
        reply_text=reply_text,
        original_subject=payload.get("original_subject", ""),
        contact_name=payload.get("contact_name", ""),
        company=payload.get("company", ""),
    )
    return result


# ──────────────────────────────────────────────
# Outreach Events
# ──────────────────────────────────────────────

@app.get("/api/outreach/events")
def list_outreach_events(
    channel: Optional[str] = None,
    status: Optional[str] = None,
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    """List outreach events with filters."""
    query = db.query(OutreachEvent)

    if channel:
        query = query.filter(OutreachEvent.channel == channel)
    if status:
        query = query.filter(OutreachEvent.status == status)

    total = query.count()
    events = query.order_by(OutreachEvent.created_at.desc()).offset(
        (page - 1) * per_page
    ).limit(per_page).all()

    return {
        "events": [
            {
                "id": e.id,
                "contact_id": e.contact_id,
                "channel": e.channel,
                "status": e.status,
                "subject": e.subject,
                "sequence_step": e.sequence_step,
                "sent_at": e.sent_at.isoformat() if e.sent_at else None,
                "opened_at": e.opened_at.isoformat() if e.opened_at else None,
                "replied_at": e.replied_at.isoformat() if e.replied_at else None,
                "is_test": e.is_test,
            }
            for e in events
        ],
        "total": total,
        "page": page,
        "per_page": per_page,
    }


# ──────────────────────────────────────────────
# Sequences
# ──────────────────────────────────────────────

@app.get("/api/sequences")
def list_sequences(db: Session = Depends(get_db)):
    """List all email sequences."""
    sequences = db.query(EmailSequence).all()
    return {
        "sequences": [
            {
                "id": s.id,
                "name": s.name,
                "description": s.description,
                "target_segment": s.target_segment,
                "is_active": s.is_active,
                "steps": [
                    {
                        "id": step.id,
                        "step_number": step.step_number,
                        "channel": step.channel,
                        "delay_days": step.delay_days,
                        "subject": step.subject,
                    }
                    for step in s.steps
                ],
            }
            for s in sequences
        ]
    }


@app.post("/api/sequences")
def create_sequence(payload: dict, db: Session = Depends(get_db)):
    """Create a new email sequence."""
    seq = EmailSequence(
        name=payload.get("name", ""),
        description=payload.get("description", ""),
        target_segment=payload.get("target_segment", ""),
    )
    db.add(seq)
    db.flush()

    for step_data in payload.get("steps", []):
        step = SequenceStep(
            sequence_id=seq.id,
            step_number=step_data.get("step_number", 1),
            channel=step_data.get("channel", "email"),
            delay_days=step_data.get("delay_days", 0),
            subject=step_data.get("subject", ""),
            body=step_data.get("body", ""),
        )
        db.add(step)

    db.commit()
    return {"status": "created", "sequence_id": seq.id}


@app.post("/api/sequences/init-sms-first")
def init_sms_first_sequences(db: Session = Depends(get_db)):
    """Initialize the SMS-first sequences in the database."""
    try:
        sequence_ids = create_sms_first_sequences(db)
        return {
            "status": "created",
            "sequences": sequence_ids,
            "message": "SMS-first sequences initialized successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create sequences: {str(e)}")


@app.post("/api/outreach/start-sms-blitz")  
def start_sms_blitz(
    limit: int = 10,
    test_mode_override: bool = False,
    db: Session = Depends(get_db),
):
    """Start SMS outreach to the top SMS-ready contacts."""
    if not settings.test_mode and not test_mode_override:
        raise HTTPException(status_code=403, detail="SMS blitz requires test mode or override")
    
    # Get SMS-ready contacts
    contacts = db.query(Contact).filter(
        Contact.sms_consent == True,
        Contact.do_not_contact == False,
        Contact.status == "ready",
        (Contact.phone != "") | (Contact.mobile != "")
    ).order_by(Contact.last_activity.desc()).limit(limit).all()
    
    if not contacts:
        return {"status": "no_contacts", "message": "No SMS-ready contacts found"}
    
    results = []
    from services.sequences import SMS_TEMPLATES
    
    for contact in contacts:
        # Use the SMS opener template
        message = SMS_TEMPLATES["opener"].format(
            first_name=contact.first_name or "there"
        )
        
        try:
            event = send_sms(db, contact, message, sequence_step=1)
            results.append({
                "contact_id": contact.id,
                "name": f"{contact.first_name} {contact.last_name}".strip(),
                "company": contact.company,
                "status": event.status,
                "event_id": event.id
            })
        except OutreachSafetyError as e:
            results.append({
                "contact_id": contact.id,
                "name": f"{contact.first_name} {contact.last_name}".strip(),
                "company": contact.company,
                "status": "error",
                "error": str(e)
            })
    
    db.commit()
    
    successful = len([r for r in results if r["status"] in ["sent", "queued"]])
    
    return {
        "status": "completed",
        "message": f"SMS blitz sent to {successful}/{len(results)} contacts",
        "results": results,
        "summary": {
            "total_attempted": len(results),
            "successful": successful,
            "failed": len(results) - successful
        }
    }


# ──────────────────────────────────────────────
# Audit Log
# ──────────────────────────────────────────────

@app.get("/api/audit")
def list_audit_log(
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    """View audit trail."""
    query = db.query(AuditLog)
    total = query.count()
    logs = query.order_by(AuditLog.timestamp.desc()).offset(
        (page - 1) * per_page
    ).limit(per_page).all()

    return {
        "logs": [
            {
                "id": l.id,
                "timestamp": l.timestamp.isoformat(),
                "action": l.action,
                "entity_type": l.entity_type,
                "entity_id": l.entity_id,
                "details": json.loads(l.details) if l.details else {},
                "user": l.user,
            }
            for l in logs
        ],
        "total": total,
        "page": page,
        "per_page": per_page,
    }


# ──────────────────────────────────────────────
# CSV Import (one-time / admin)
# ──────────────────────────────────────────────

@app.post("/api/admin/import-csv")
def import_csv_endpoint(db: Session = Depends(get_db)):
    """Import the cleaned CSV into the database."""
    csv_path = os.path.join(
        os.path.dirname(__file__), '..', 'data', 'contacts-cleaned.csv'
    )
    if not os.path.exists(csv_path):
        raise HTTPException(status_code=404, detail="Cleaned CSV not found. Run clean_csv.py first.")

    from services.import_contacts import import_csv_to_db
    stats = import_csv_to_db(db, csv_path)
    db.commit()
    return {"status": "imported", "stats": stats}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=settings.app_port, reload=True)
