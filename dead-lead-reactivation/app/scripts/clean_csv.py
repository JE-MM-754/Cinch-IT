#!/usr/bin/env python3
"""
Clean and normalize the raw CinchIT contact CSV.
Output: cleaned CSV with standardized fields, ready for enrichment.
"""

import csv
import re
import os
from datetime import datetime

RAW_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw-contacts.csv')
CLEAN_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'contacts-cleaned.csv')

def normalize_phone(phone: str) -> str:
    """Strip to digits, format as +1XXXXXXXXXX if US number."""
    if not phone:
        return ''
    digits = re.sub(r'\D', '', phone)
    if len(digits) == 10:
        digits = '1' + digits
    if len(digits) == 11 and digits.startswith('1'):
        return f'+{digits}'
    return phone.strip()  # Return original if we can't parse

def normalize_name(contact: str) -> tuple:
    """Parse 'last, first' into (first_name, last_name)."""
    if not contact or ',' not in contact:
        return ('', contact.strip() if contact else '')
    parts = contact.split(',', 1)
    last = parts[0].strip()
    first = parts[1].strip()
    return (first, last)

def normalize_email(email: str) -> str:
    """Lowercase and strip whitespace."""
    if not email:
        return ''
    email = email.strip().lower()
    # Basic validation
    if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        return email
    return ''  # Invalid email

def parse_date(date_str: str) -> str:
    """Parse M/D/YY to YYYY-MM-DD."""
    if not date_str:
        return ''
    try:
        dt = datetime.strptime(date_str.strip(), '%m/%d/%y')
        return dt.strftime('%Y-%m-%d')
    except ValueError:
        return date_str.strip()

def classify_contact(row: dict) -> str:
    """
    Classify: ready | needs_enrichment | do_not_contact
    SMS-FIRST STRATEGY:
    - ready: has phone/mobile (SMS is primary channel)
    - needs_enrichment: missing phone AND email
    - do_not_contact: placeholder for manual/future flags
    """
    has_phone = row['phone'] or row['mobile']
    has_email = row['email']
    
    if has_phone:  # SMS-ready contacts are priority
        return 'ready'
    elif has_email:  # Email-only contacts are secondary
        return 'ready'
    else:
        return 'needs_enrichment'

def main():
    rows = []
    with open(RAW_PATH, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for r in reader:
            first, last = normalize_name(r.get('Contact', ''))
            phone = normalize_phone(r.get('Phone', ''))
            mobile = normalize_phone(r.get('Mobile Phone', ''))
            email = normalize_email(r.get('Email', ''))
            company = r.get('Client', '').strip()
            last_activity = parse_date(r.get('Last Activity', ''))
            extension = r.get('Extension', '').strip()
            classification = r.get('Classification', '').strip()

            cleaned = {
                'first_name': first,
                'last_name': last,
                'company': company,
                'email': email,
                'phone': phone,
                'mobile': mobile,
                'extension': extension,
                'last_activity': last_activity,
                'original_classification': classification,
                'status': '',  # set below
                'enrichment_needed': '',
                'apollo_enriched': 'no',
                'business_verified': 'no',
                'do_not_contact': 'no',
                'notes': ''
            }
            cleaned['status'] = classify_contact(cleaned)

            # Flag what enrichment is needed (SMS-first priority)
            missing = []
            if not phone and not mobile:
                missing.append('phone')  # Phone is now #1 priority
            if not email:
                missing.append('email')   # Email is secondary
            cleaned['enrichment_needed'] = ','.join(missing) if missing else 'none'

            rows.append(cleaned)

    # Deduplicate by company + last_name (keep most recent activity)
    seen = {}
    for row in rows:
        key = (row['company'].lower(), row['last_name'].lower(), row['first_name'].lower())
        if key in seen:
            existing = seen[key]
            if row['last_activity'] > existing['last_activity']:
                seen[key] = row
        else:
            seen[key] = row

    deduped = list(seen.values())
    deduped.sort(key=lambda x: x['last_activity'], reverse=True)

    # Write clean CSV
    fieldnames = [
        'first_name', 'last_name', 'company', 'email', 'phone', 'mobile',
        'extension', 'last_activity', 'original_classification', 'status',
        'enrichment_needed', 'apollo_enriched', 'business_verified',
        'do_not_contact', 'notes'
    ]
    with open(CLEAN_PATH, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(deduped)

    # Stats
    total = len(deduped)
    ready = sum(1 for r in deduped if r['status'] == 'ready')
    needs_enrichment = sum(1 for r in deduped if r['status'] == 'needs_enrichment')
    unique_companies = len(set(r['company'].lower() for r in deduped if r['company']))

    print(f"=== CSV Cleaning Complete ===")
    print(f"Raw rows: {len(rows)}")
    print(f"After dedup: {total}")
    print(f"Unique companies: {unique_companies}")
    print(f"Ready (has email): {ready}")
    print(f"Needs enrichment: {needs_enrichment}")
    print(f"Output: {CLEAN_PATH}")

if __name__ == '__main__':
    main()
