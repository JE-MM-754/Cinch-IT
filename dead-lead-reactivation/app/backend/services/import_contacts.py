"""
Import cleaned CSV into the database.
"""

import csv
import json
import os
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from models import Contact, AuditLog


def import_csv_to_db(db: Session, csv_path: str) -> dict:
    """
    Import cleaned CSV into contacts table.
    Returns stats dict.
    """
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV not found: {csv_path}")

    stats = {"imported": 0, "skipped_duplicate": 0, "errors": 0}

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Check for duplicate (company + last_name + first_name)
            existing = db.query(Contact).filter(
                Contact.company == row.get('company', ''),
                Contact.last_name == row.get('last_name', ''),
                Contact.first_name == row.get('first_name', ''),
            ).first()

            if existing:
                stats["skipped_duplicate"] += 1
                continue

            try:
                # SMS-FIRST STRATEGY: Assume SMS consent for imported leads
                # These are Cinch IT's previous business inquiries, not cold contacts
                has_phone = bool(row.get('phone', '') or row.get('mobile', ''))
                
                contact = Contact(
                    first_name=row.get('first_name', ''),
                    last_name=row.get('last_name', ''),
                    company=row.get('company', ''),
                    email=row.get('email', ''),
                    phone=row.get('phone', ''),
                    mobile=row.get('mobile', ''),
                    extension=row.get('extension', ''),
                    last_activity=row.get('last_activity', ''),
                    status=row.get('status', 'needs_enrichment'),
                    do_not_contact=(row.get('do_not_contact', 'no') == 'yes'),
                    apollo_enriched=(row.get('apollo_enriched', 'no') == 'yes'),
                    business_verified=(row.get('business_verified', 'no') == 'yes'),
                    notes=row.get('notes', ''),
                    # SMS CONSENT: True if they have a phone number (previous business inquiry)
                    sms_consent=has_phone,
                    email_consent=True,  # B2B email implied consent
                    voice_consent=False,  # Voice requires explicit consent
                )
                db.add(contact)
                stats["imported"] += 1
            except Exception as e:
                stats["errors"] += 1

    db.flush()

    # Audit log
    audit = AuditLog(
        action="csv_imported",
        entity_type="contact",
        entity_id=None,
        details=json.dumps({"csv_path": csv_path, "stats": stats}),
        user="system",
    )
    db.add(audit)

    return stats
