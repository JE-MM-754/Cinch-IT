"""Database models for the Dead Lead Reactivation system."""

from sqlalchemy import (
    Column, Integer, String, DateTime, Boolean, Text, Float,
    ForeignKey, Enum, Index, create_engine
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime, timezone
import enum

Base = declarative_base()


class ContactStatus(str, enum.Enum):
    READY = "ready"
    NEEDS_ENRICHMENT = "needs_enrichment"
    DO_NOT_CONTACT = "do_not_contact"


class OutreachChannel(str, enum.Enum):
    EMAIL = "email"
    SMS = "sms"
    VOICE = "voice"


class OutreachStatus(str, enum.Enum):
    QUEUED = "queued"
    SENT = "sent"
    DELIVERED = "delivered"
    OPENED = "opened"
    CLICKED = "clicked"
    REPLIED = "replied"
    BOUNCED = "bounced"
    UNSUBSCRIBED = "unsubscribed"
    FAILED = "failed"


class ResponseType(str, enum.Enum):
    INTERESTED = "interested"
    NOT_INTERESTED = "not_interested"
    WRONG_PERSON = "wrong_person"
    OUT_OF_OFFICE = "out_of_office"
    UNSUBSCRIBE = "unsubscribe"
    UNKNOWN = "unknown"


class MeetingStatus(str, enum.Enum):
    SCHEDULED = "scheduled"
    COMPLETED = "completed"
    NO_SHOW = "no_show"
    CANCELLED = "cancelled"
    RESCHEDULED = "rescheduled"


class Contact(Base):
    """A contact from Cinch IT's dead lead database."""
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(100), default='')
    last_name = Column(String(100), default='')
    company = Column(String(255), default='')
    email = Column(String(255), default='')
    phone = Column(String(20), default='')
    mobile = Column(String(20), default='')
    extension = Column(String(10), default='')
    last_activity = Column(String(10), default='')  # YYYY-MM-DD from original data

    # Classification
    status = Column(String(20), default='needs_enrichment')
    do_not_contact = Column(Boolean, default=False)
    do_not_contact_reason = Column(Text, default='')

    # Enrichment
    apollo_enriched = Column(Boolean, default=False)
    enriched_at = Column(DateTime, nullable=True)
    business_verified = Column(Boolean, default=False)
    business_active = Column(Boolean, nullable=True)  # None = unknown
    enrichment_data = Column(Text, default='{}')  # JSON blob from Apollo

    # Outreach state
    email_consent = Column(Boolean, default=True)  # B2B email = implied consent
    sms_consent = Column(Boolean, default=False)   # Must be earned
    voice_consent = Column(Boolean, default=False)  # Must be earned
    current_sequence_step = Column(Integer, default=0)
    last_outreach_at = Column(DateTime, nullable=True)
    next_outreach_at = Column(DateTime, nullable=True)

    # Metadata
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc))
    notes = Column(Text, default='')

    # Relationships
    outreach_events = relationship("OutreachEvent", back_populates="contact")
    meetings = relationship("Meeting", back_populates="contact")

    __table_args__ = (
        Index('idx_contact_status', 'status'),
        Index('idx_contact_email', 'email'),
        Index('idx_contact_company', 'company'),
        Index('idx_next_outreach', 'next_outreach_at'),
    )


class OutreachEvent(Base):
    """A single outreach touchpoint (email, SMS, or voice call)."""
    __tablename__ = "outreach_events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    contact_id = Column(Integer, ForeignKey('contacts.id'), nullable=False)
    channel = Column(String(10), nullable=False)  # email, sms, voice
    status = Column(String(20), default='queued')
    sequence_step = Column(Integer, default=1)

    # Content
    subject = Column(String(255), default='')  # Email subject
    body = Column(Text, default='')  # Email body or SMS text
    template_id = Column(String(50), default='')

    # Tracking
    sent_at = Column(DateTime, nullable=True)
    delivered_at = Column(DateTime, nullable=True)
    opened_at = Column(DateTime, nullable=True)
    clicked_at = Column(DateTime, nullable=True)
    replied_at = Column(DateTime, nullable=True)
    bounced_at = Column(DateTime, nullable=True)

    # Response handling
    response_type = Column(String(20), nullable=True)
    response_body = Column(Text, default='')
    ai_classification = Column(Text, default='')  # AI's analysis of the response

    # Provider tracking
    provider_message_id = Column(String(255), default='')  # SendGrid/Twilio message ID

    # Metadata
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    is_test = Column(Boolean, default=False)  # True = sent to Jamie's test contact

    # Relationships
    contact = relationship("Contact", back_populates="outreach_events")

    __table_args__ = (
        Index('idx_outreach_contact', 'contact_id'),
        Index('idx_outreach_status', 'status'),
        Index('idx_outreach_sent', 'sent_at'),
    )


class Meeting(Base):
    """A meeting booked from a reactivated lead."""
    __tablename__ = "meetings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    contact_id = Column(Integer, ForeignKey('contacts.id'), nullable=False)
    scheduled_at = Column(DateTime, nullable=False)
    duration_minutes = Column(Integer, default=30)
    status = Column(String(20), default='scheduled')
    calendar_event_id = Column(String(255), default='')
    assigned_to = Column(String(100), default='')  # Jack Wilson, etc.
    notes = Column(Text, default='')
    outcome = Column(Text, default='')  # Post-meeting notes

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc))

    contact = relationship("Contact", back_populates="meetings")

    __table_args__ = (
        Index('idx_meeting_scheduled', 'scheduled_at'),
        Index('idx_meeting_status', 'status'),
    )


class EmailSequence(Base):
    """Email sequence templates."""
    __tablename__ = "email_sequences"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, default='')
    target_segment = Column(String(50), default='')  # e.g., '2020_churn', '2021_2022_churn'
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    steps = relationship("SequenceStep", back_populates="sequence", order_by="SequenceStep.step_number")


class SequenceStep(Base):
    """Individual step in an email sequence."""
    __tablename__ = "sequence_steps"

    id = Column(Integer, primary_key=True, autoincrement=True)
    sequence_id = Column(Integer, ForeignKey('email_sequences.id'), nullable=False)
    step_number = Column(Integer, nullable=False)
    channel = Column(String(10), default='email')  # email, sms, voice
    delay_days = Column(Integer, default=0)  # Days after previous step
    subject = Column(String(255), default='')
    body = Column(Text, default='')
    is_active = Column(Boolean, default=True)

    sequence = relationship("EmailSequence", back_populates="steps")


class AuditLog(Base):
    """Audit trail for compliance — every action on contact data is logged."""
    __tablename__ = "audit_log"

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    action = Column(String(50), nullable=False)  # e.g., 'email_sent', 'contact_enriched', 'data_exported'
    entity_type = Column(String(50), default='')  # 'contact', 'outreach_event', etc.
    entity_id = Column(Integer, nullable=True)
    details = Column(Text, default='{}')  # JSON details
    user = Column(String(100), default='system')

    __table_args__ = (
        Index('idx_audit_timestamp', 'timestamp'),
        Index('idx_audit_entity', 'entity_type', 'entity_id'),
    )


def init_db(database_url: str = "sqlite:///./cinchit.db"):
    """Initialize database and create all tables."""
    engine = create_engine(database_url, echo=False)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return engine, Session
