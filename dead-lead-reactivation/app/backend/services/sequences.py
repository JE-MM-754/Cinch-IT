"""
SMS-First Reactivation Sequences for Cinch IT Dead Leads
Built for Jamie's thesis: SMS gets 98% open rates vs 20% email
"""

from typing import List, Dict
from sqlalchemy.orm import Session
from models import EmailSequence, SequenceStep

def create_sms_first_sequences(db: Session) -> List[int]:
    """
    Create SMS-first reactivation sequences.
    Returns list of sequence IDs created.
    """
    sequences = []
    
    # Sequence 1: Quick Check-In (Primary SMS sequence)
    seq1 = EmailSequence(
        name="SMS-First Quick Check-In",
        description="Primary SMS-first reactivation for leads with phone numbers. Fast, direct, personal.",
        target_segment="dead_leads_with_phone",
        is_active=True
    )
    db.add(seq1)
    db.flush()
    
    # Step 1: SMS opener (Day 0)
    step1 = SequenceStep(
        sequence_id=seq1.id,
        step_number=1,
        channel="sms",
        delay_days=0,
        subject="",  # SMS has no subject
        body="Hi {first_name}, Jamie from Cinch IT here. Know you looked at managed IT services a while back. Still something you're thinking about? Quick 2-min call to see if we can help. -Jamie",
        is_active=True
    )
    db.add(step1)
    
    # Step 2: Email with value (Day 2 - after SMS breaks the ice)
    step2 = SequenceStep(
        sequence_id=seq1.id,
        step_number=2,
        channel="email",
        delay_days=2,
        subject="Quick follow-up from Jamie at Cinch IT",
        body="""Hi {first_name},

I texted you earlier about managed IT services. Since you looked into this before, thought you might find this interesting:

We just helped a {company_similar} save $2,400/month on their IT costs while improving their security and uptime. The owner told me it was "the best business decision we made this year."

Three things we did:
• Moved them from break-fix to proactive monitoring (90% fewer emergencies)  
• Upgraded their cybersecurity (they were one ransomware click away from disaster)
• Streamlined their systems (employees are way more productive)

Worth a quick 15-minute call to see if there's a fit for {company}?

Best regards,
Jamie Erickson
VP Sales & Customer Delivery
Cinch IT Boston
508-404-9628""",
        is_active=True
    )
    db.add(step2)
    
    # Step 3: SMS follow-up (Day 5)
    step3 = SequenceStep(
        sequence_id=seq1.id,
        step_number=3,
        channel="sms",
        delay_days=5,
        subject="",
        body="Hey {first_name}, sent some info Tuesday about how we saved {company_similar} $2,400/month on IT. Worth a quick 5-min call? Same number: 508-404-9628. -Jamie",
        is_active=True
    )
    db.add(step3)
    
    # Step 4: Final email value-add (Day 10)
    step4 = SequenceStep(
        sequence_id=seq1.id,
        step_number=4,
        channel="email",
        delay_days=10,
        subject="Last note from Jamie at Cinch IT",
        body="""Hi {first_name},

I know you're busy, so I'll keep this short.

Since you inquired about managed IT before, I wanted to share one thing that might save you from a major headache:

**Most small businesses are sitting ducks for ransomware.** We see it constantly - companies get hit, lose weeks of work, and pay $10-50K in ransom (if they're lucky).

The good news? It's totally preventable for about $200/month.

If that sounds interesting, here's my calendar: [calendar link]

If not, no worries - I'll stop bothering you. Just hit reply and say "not interested" and I'll remove you from my list.

Either way, hope {company} is doing well.

Best,
Jamie Erickson
Cinch IT Boston""",
        is_active=True
    )
    db.add(step4)
    
    sequences.append(seq1.id)
    
    # Sequence 2: Email-Only Fallback (for contacts without SMS consent)
    seq2 = EmailSequence(
        name="Email-Only Reactivation",
        description="Traditional email sequence for contacts without phone numbers",
        target_segment="dead_leads_email_only",
        is_active=True
    )
    db.add(seq2)
    db.flush()
    
    # Email-only sequence (traditional approach)
    email_steps = [
        {
            "step": 1, "delay": 0, "subject": "Jamie from Cinch IT - quick question",
            "body": """Hi {first_name},

Jamie from Cinch IT here. I noticed you looked into managed IT services for {company} a while back.

Just curious - is that still on your radar?

We've been helping Boston-area businesses like yours eliminate IT headaches and save money. Most of our clients wish they'd called us sooner.

Worth a quick 15-minute conversation?

Best regards,
Jamie Erickson
VP Sales & Customer Delivery
Cinch IT Boston
508-404-9628"""
        },
        {
            "step": 2, "delay": 4, "subject": "How we saved {company_similar} $2,400/month",
            "body": """Hi {first_name},

Quick follow-up on managed IT services for {company}.

I thought you'd find this interesting: we just helped a {company_similar} in the same industry save $2,400/month on IT while dramatically improving their security and reliability.

Here's what we did:
• Moved them from "break-fix" to proactive monitoring (90% fewer IT fires)
• Implemented enterprise-grade cybersecurity (sleep better at night)
• Streamlined their systems (employees are 30% more productive)

The owner told me: "Best business decision we made this year."

Worth exploring for {company}? 

Here's my calendar: [calendar link]

Best,
Jamie"""
        },
        {
            "step": 3, "delay": 8, "subject": "Last note about {company}'s IT",
            "body": """Hi {first_name},

I'll keep this brief since I know you're swamped.

One quick thing about {company}'s IT situation:

Most businesses our size are one click away from a ransomware attack. We see it constantly - companies lose weeks of work and pay $10-50K in ransom.

The crazy part? It's totally preventable for about $200/month.

If that's worth 15 minutes of discussion, here's my calendar: [calendar link]

If not, no problem - just hit reply and say "not interested" and I'll stop following up.

Hope business is going well either way.

Jamie Erickson
Cinch IT Boston"""
        }
    ]
    
    for step_data in email_steps:
        step = SequenceStep(
            sequence_id=seq2.id,
            step_number=step_data["step"],
            channel="email",
            delay_days=step_data["delay"],
            subject=step_data["subject"],
            body=step_data["body"],
            is_active=True
        )
        db.add(step)
    
    sequences.append(seq2.id)
    
    # Sequence 3: High-Value Prospects (for contacts with recent activity)
    seq3 = EmailSequence(
        name="High-Value SMS Blitz",
        description="Aggressive SMS-heavy sequence for recent high-value prospects",
        target_segment="recent_high_value_leads",
        is_active=True
    )
    db.add(seq3)
    db.flush()
    
    # High-value sequence (more aggressive)
    high_value_steps = [
        {"step": 1, "channel": "sms", "delay": 0, "body": "Hi {first_name}, Jamie from Cinch IT. Saw you were looking at managed IT recently. Are you still evaluating options? Quick call this week? -Jamie 508-404-9628"},
        {"step": 2, "channel": "email", "delay": 1, "subject": "Following up on Cinch IT conversation", "body": "Hi {first_name},\n\nI texted you yesterday about managed IT services.\n\nSince you were actively looking recently, I wanted to get on your calendar ASAP. We're booking March implementations now, and I'd hate for you to get pushed to Q2.\n\nHere's my calendar: [calendar link]\n\nOr just text me back at 508-404-9628.\n\nBest,\nJamie"},
        {"step": 3, "channel": "sms", "delay": 3, "body": "Hey {first_name}, still interested in managed IT for {company}? March implementations are filling up. Worth a quick chat? -Jamie"},
        {"step": 4, "channel": "email", "delay": 7, "subject": "One more try - {company}'s IT", "body": "Hi {first_name},\n\nI've reached out a few times about managed IT for {company}.\n\nMaybe the timing isn't right, or maybe I'm not the right fit. That's totally fine.\n\nBut if you're still looking at options, I'd love 15 minutes to show you how we're different.\n\nIf not, just hit reply and say 'not interested' and I'll leave you alone.\n\nBest,\nJamie"}
    ]
    
    for step_data in high_value_steps:
        step = SequenceStep(
            sequence_id=seq3.id,
            step_number=step_data["step"],
            channel=step_data["channel"],
            delay_days=step_data["delay"],
            subject=step_data.get("subject", ""),
            body=step_data["body"],
            is_active=True
        )
        db.add(step)
    
    sequences.append(seq3.id)
    
    db.commit()
    return sequences


def get_best_sequence_for_contact(contact) -> str:
    """
    Choose the best sequence for a contact based on their profile.
    SMS-first strategy prioritizes contacts with phone numbers.
    """
    has_phone = bool(contact.phone or contact.mobile)
    has_email = bool(contact.email)
    
    # Parse last activity date to determine recency
    last_activity = contact.last_activity  # YYYY-MM-DD format
    is_recent = False
    if last_activity:
        try:
            from datetime import datetime
            activity_date = datetime.strptime(last_activity, '%Y-%m-%d')
            now = datetime.now()
            days_since = (now - activity_date).days
            is_recent = days_since < 365  # Within last year = recent
        except:
            pass
    
    # Decision logic
    if has_phone and contact.sms_consent:
        if is_recent:
            return "High-Value SMS Blitz"  # Aggressive for recent prospects
        else:
            return "SMS-First Quick Check-In"  # Standard SMS sequence
    elif has_email:
        return "Email-Only Reactivation"  # Fallback to email
    else:
        return None  # Need enrichment first


# Message templates for dynamic content
SMS_TEMPLATES = {
    "opener": "Hi {first_name}, Jamie from Cinch IT here. Know you looked at managed IT services a while back. Still something you're thinking about? Quick 2-min call to see if we can help. -Jamie",
    "follow_up": "Hey {first_name}, sent some info Tuesday about how we saved {company_similar} $2,400/month on IT. Worth a quick 5-min call? Same number: 508-404-9628. -Jamie",
    "urgent": "Hi {first_name}, Jamie from Cinch IT. Saw you were looking at managed IT recently. Are you still evaluating options? Quick call this week? -Jamie 508-404-9628",
    "final": "Hey {first_name}, still interested in managed IT for {company}? March implementations are filling up. Worth a quick chat? -Jamie"
}

EMAIL_TEMPLATES = {
    "opener_subject": "Jamie from Cinch IT - quick question",
    "case_study_subject": "How we saved {company_similar} $2,400/month",
    "final_subject": "Last note about {company}'s IT",
    "urgent_subject": "Following up on Cinch IT conversation"
}