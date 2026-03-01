# Dead Lead AI Reactivation — Project Plan Notes

*Started: 2026-02-26*
*Status: Discovery / Requirements Gathering*

---

## CSV Data Schema (655 rows, 654 contacts + header)
| Column | Coverage | Notes |
|--------|----------|-------|
| Classification | 0% (all empty) | No lead scoring/tagging exists |
| Contact | 100% | Name (last, first format) |
| Client | ~100% | Company name — 456 unique companies |
| Phone | 92% (606) | Business phone |
| Extension | Sparse | |
| Mobile Phone | 4% (29) | Almost useless for SMS without enrichment |
| Last Activity | 100% | Date of last interaction |
| Email | 51% (336) | Half the database has no email — needs enrichment |

### Activity Distribution
- 2017: 3 | 2018: 69 | 2019: 43 | **2020: 370 (56%)** | 2021: 44 | 2022: 34 | 2023: 14 | 2024: 15 | 2025: 63

### Key Data Gaps
- **No email for 49% of contacts** — enrichment required before outreach
- **No mobile for 96%** — SMS channel requires enrichment or opt-in collection
- **No classification/tags** — we have to build our own scoring
- **No service history, contract value, or churn reason** — ask Jay for richer export

---

## Answers from Jamie (2026-02-26)

1. **CSV is confirmed dead leads only.** Got in December. More exports available from ConnectWise. Richer data may exist in their systems — investigate on-site.
2. **Schema:** 8 columns (see above). Thin data — enrichment is mandatory.
3. **CRM beyond ConnectWise:** Unknown. → **ASK ON-SITE**
4. **Current outreach stack:** Unknown. We're handling all outreach for this use case.
5. **Email authentication (SPF/DKIM/DMARC):** Unknown. We're handling all email infra.
6. **Channels: Email + SMS + AI Voice.** Need to understand compliance implications for each and discuss on-site.
7. **Sender:** Virtual agent inbox. Sends email, SMS, voice. Books meetings directly on reps' calendars.
8. **Data storage:** CSV on Jamie's machine only. They can send more exports via CSV.
9. **Data processing agreements:** Exist but need to review. → **ASK ON-SITE**
10. **Contact type:** Largely B2B. Good — fewer compliance restrictions.
11. **Rev share:** 50% is Jamie's target. Not yet agreed with Jay.
12. **Average MRR per client:** Unknown. → **ASK ON-SITE**

---

## Security Requirements (Non-Negotiable)

### Data Handling
- All contact data encrypted at rest (AES-256) and in transit (TLS 1.3)
- No PII stored in plaintext on any server
- CSV imports processed and encrypted immediately — raw CSVs purged after import
- Role-based access control — only Jamie and authorized Cinch IT users see data
- Audit log for every data access, modification, and outreach action
- Data retention policy: define with Jay (suggest 24-month rolling window, then purge)

### Email Compliance (CAN-SPAM)
- Every email must include: physical mailing address, clear unsubscribe mechanism, accurate sender/subject
- Unsubscribe requests honored within 10 business days
- No purchased email lists — these are Cinch IT's own contacts (we're good)
- Dedicated sending domain (NOT cinchit.com — protect their main domain reputation)
- Warm up sending domain 2-3 weeks before full blast

### SMS Compliance (TCPA)
- **Prior express consent required for marketing SMS** — this is the big one
- Dead leads from 2020 likely did NOT opt in to SMS → **cannot cold-text them**
- Options: (a) email first to collect SMS opt-in, (b) only SMS contacts who respond/opt in, (c) use SMS only for leads who engage first
- Must include opt-out mechanism in every SMS
- → **Discuss consent strategy on-site with Jay**

### Voice/AI Calling Compliance (TCPA + FCC)
- Prerecorded/AI voice calls to cell phones require **prior express written consent**
- Calls to business landlines for B2B purposes: more permissible but still need care
- Must comply with Do Not Call registry
- Caller ID must be accurate (no spoofing)
- → **Recommend: AI voice only for warm leads who've already engaged via email**

### Infrastructure Security
- Hosted on SOC 2-compliant cloud provider (AWS/GCP)
- No API keys in source code — use secrets manager (AWS Secrets Manager, Vault, etc.)
- All third-party integrations via OAuth where possible
- Regular dependency audits (Snyk/Dependabot)
- Penetration testing before go-live (even a basic one)

---

## Architecture (High-Level)

```
[CSV Import] → [Data Pipeline: Clean + Enrich + Score]
                         ↓
              [Secure Contact Database (encrypted)]
                         ↓
         [Outreach Orchestrator: Email / SMS / Voice]
                    ↓         ↓          ↓
              [Mailgun/    [Twilio    [Twilio/Bland.ai
               SendGrid]    SMS]       Voice]
                         ↓
              [Response Handler + Meeting Booker]
                         ↓
              [Calendar Integration (Calendly/Cal.com)]
                         ↓
              [Dashboard: Campaign Analytics + ROI]
```

### Tech Stack (Proposed)
- **Backend:** Python (FastAPI) or Node.js
- **Database:** PostgreSQL with encryption at rest
- **Email:** SendGrid or Mailgun (deliverability + compliance built in)
- **SMS:** Twilio (TCPA-compliant tooling built in)
- **Voice:** Bland.ai or Twilio + ElevenLabs (AI voice agent)
- **Enrichment:** Apollo.io, Clearbit, or ZoomInfo (for missing emails/phones)
- **Calendar:** Cal.com or Calendly API
- **Hosting:** AWS or GCP (SOC 2 compliant)
- **Auth:** Clerk or Auth0 (RBAC)
- **Monitoring:** Sentry + basic logging

---

## Testing Contact Info
- **Name:** Jamie Erickson
- **Phone:** 508-404-9628
- **Email:** Erickson.JamesD@gmail.com

## Sales Methodology: Challenger Sale
- All outreach scripts follow Challenger Sale methodology
- Teach → Tailor → Take Control
- Lead with insight, not product. Challenge their assumptions about their IT security posture.
- **TODO:** Review scripts with Jamie tomorrow — edit together

## ⛔ OUTREACH SAFETY GATE (NON-NEGOTIABLE)

**All outreach testing uses Jamie's contact info ONLY.**
- Name: Jamie Erickson
- No live contacts are touched until Jamie explicitly approves go-live.
- This gate applies to email, SMS, AND voice channels.
- No exceptions. No "just one test." Jamie says go, or it doesn't go.

---

## Phases

### Phase 1: Data Enrichment & Scoring (Week 1)
- Import CSV, clean data, deduplicate
- Enrich missing emails and phone numbers
- Verify business is still operating (Google Maps API, website check)
- Score/tier contacts by reactivation potential
- Build suppression list (already customers, out of business, do-not-contact)

### Phase 2: Email Campaign (Week 2-3)
- Set up dedicated sending domain + warm it up
- Build email sequences (3-5 touch, pain-point specific)
- Deploy to Tier 1 (2020-2022) contacts with email
- Track opens, clicks, replies
- Auto-route replies to response handler

### Phase 3: SMS + Voice (Week 3-4)
- SMS only to contacts who engaged with email (opt-in flow)
- AI voice follow-up for high-intent leads
- Meeting booking automation
- Handoff to Cinch IT sales team

### Phase 4: Reporting & Optimization (Ongoing)
- Campaign dashboard with real-time metrics
- A/B test messaging, timing, channels
- Weekly reports to Jay/Jack
- Iterate based on conversion data

---

## Decisions (2026-02-26 5:39 PM)

- **Apollo account:** erickson.jamesd754@icloud.com
- **Domain:** getcinchmsp.com (ping Discord if unavailable)
- **Infra:** Fresh setup (AWS or GCP)
- **Repo:** Build in workspace for now. GitHub setup = medium priority (remind Jamie until done)
- **Secrets:** Local .env file (not committed)
- **Email service:** Sign up NOW — start warming immediately
- **Twilio:** Sign up NOW
- **Tech stack:** My call — optimizing for speed + security
- **Deadline:** Working version of Project 1 ready for review 2026-02-27
- **Sales methodology:** Challenger Sale (review scripts together tomorrow)
- **.env location:** `/Users/jameserickson/Desktop/Business Ventures/Cinch IT/dead-lead-reactivation/app/.env`

## Questions for On-Site Meeting with Jay
→ See: `../onsite-discovery-questions.md`
