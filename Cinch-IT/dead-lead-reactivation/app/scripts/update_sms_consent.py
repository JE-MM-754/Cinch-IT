#!/usr/bin/env python3
"""
Update existing contacts to enable SMS consent for SMS-first strategy.
Run this to retrofit existing database with SMS consent based on phone numbers.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from database import get_db_session
from models import Contact, AuditLog
import json
from datetime import datetime, timezone

def main():
    """Update SMS consent for contacts with phone numbers."""
    print("Updating contacts for SMS-first strategy...")
    
    with get_db_session() as db:
        # Find contacts with phone numbers but no SMS consent
        contacts_to_update = db.query(Contact).filter(
            (Contact.phone != "") | (Contact.mobile != ""),
            Contact.sms_consent == False
        ).all()
        
        print(f"Found {len(contacts_to_update)} contacts with phone numbers to update")
        
        updated_count = 0
        
        for contact in contacts_to_update:
            # Enable SMS consent for contacts with phone numbers
            # (Jamie's thesis: these are previous business inquiries)
            contact.sms_consent = True
            
            # If they now have SMS consent, they're probably ready
            if contact.status == "needs_enrichment" and (contact.phone or contact.mobile):
                contact.status = "ready"
            
            # Audit log
            audit = AuditLog(
                action="sms_consent_enabled",
                entity_type="contact",
                entity_id=contact.id,
                details=json.dumps({
                    "reason": "SMS-first strategy retrofit",
                    "has_phone": bool(contact.phone),
                    "has_mobile": bool(contact.mobile),
                    "previous_status": contact.status
                }),
                user="system"
            )
            db.add(audit)
            
            updated_count += 1
        
        print(f"✅ Updated {updated_count} contacts with SMS consent")
        
        # Show summary stats
        total_contacts = db.query(Contact).count()
        sms_ready = db.query(Contact).filter(
            Contact.sms_consent == True,
            (Contact.phone != "") | (Contact.mobile != "")
        ).count()
        email_only = db.query(Contact).filter(
            Contact.sms_consent == False,
            Contact.email != ""
        ).count()
        ready_contacts = db.query(Contact).filter(Contact.status == "ready").count()
        
        print(f"\nUpdated database stats:")
        print(f"- Total contacts: {total_contacts}")
        print(f"- SMS-ready contacts: {sms_ready}")
        print(f"- Email-only contacts: {email_only}")
        print(f"- Ready for outreach: {ready_contacts}")
        print(f"\n🚀 SMS-first strategy is ready!")

if __name__ == '__main__':
    main()