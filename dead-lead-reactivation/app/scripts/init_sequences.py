#!/usr/bin/env python3
"""
Initialize SMS-first reactivation sequences in the database.
Run this after importing contacts to set up the outreach sequences.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from database import get_db_session
from services.sequences import create_sms_first_sequences

def main():
    """Initialize all SMS-first sequences."""
    print("Creating SMS-first reactivation sequences...")
    
    with get_db_session() as db:
        sequence_ids = create_sms_first_sequences(db)
        
        print(f"\n✅ Created {len(sequence_ids)} sequences:")
        print("1. SMS-First Quick Check-In (primary SMS sequence)")
        print("2. Email-Only Reactivation (fallback for no SMS consent)")
        print("3. High-Value SMS Blitz (aggressive for recent prospects)")
        
        # Verify sequences were created
        from models import EmailSequence, SequenceStep
        total_sequences = db.query(EmailSequence).count()
        total_steps = db.query(SequenceStep).count()
        
        print(f"\nDatabase now has:")
        print(f"- {total_sequences} sequences total")
        print(f"- {total_steps} sequence steps total")
        
        print(f"\nSequence IDs created: {sequence_ids}")
        print("\n🚀 Ready for SMS-first outreach!")

if __name__ == '__main__':
    main()