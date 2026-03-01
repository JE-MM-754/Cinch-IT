# AI Prospecting Engine — Project Plan Notes

*Started: 2026-02-26*
*Status: Discovery / Requirements Gathering*

---

## What Jack Wilson Asked For (Sep 11, 2025 Email)

> "We used Lantern to find your top 25 prospects most urgent needs (flagging compliance issues, funding, recent hiring surges). If your tool could uncover the pain points we talked about for us, THAT would be awesome."

**Translation:** Jack wants an AI system that:
1. Identifies the most promising prospects in a target geography
2. Detects *why* they need IT services *right now* (not just who they are)
3. Generates actionable intelligence — not just a list, but the *approach angle*

---

## Answers from Jamie (2026-02-26)

13. **Pain point signals:** Not fully defined. Jack mentioned compliance + hiring surges. Building expanded signal list below from his email context.
14. **ICP:** Building draft — see `cinch-it-icp.md`
15. **Scope:** Net-new prospecting only (for now)
16. **Deployment:** Standalone web app
17. **End users:** Jack Wilson + Jamie initially. Roll out to full sales team once proven.
18. **Signal refresh:** Daily batch
19. **Data sources:** "Use anything" — Jamie's directive. **My pushback below.**
20. **Budget for APIs:** TBD after mockup. Options listed below.

---

## Pushback on Data Sources (Q19)

Jamie said "use anything." I disagree partially. Here's why:

**Cinch IT is an IT services company.** Their prospects are SMBs who trust them with their technology and data security. If it ever came out that Cinch IT's prospecting tool was scraping LinkedIn or violating data ToS, it would be a reputational disaster. The bar is higher for an MSP than a random startup.

**What I recommend:**
- ✅ **Public data:** Business registrations, SEC filings, job postings (Indeed/LinkedIn Jobs API), news, press releases, Google Maps/Yelp business listings
- ✅ **Licensed APIs:** Apollo.io, ZoomInfo, Clearbit, Crunchbase — these have legitimate data licensing
- ✅ **Government/regulatory data:** OSHA, state compliance databases, SBA data
- ⚠️ **LinkedIn:** Only via official API or Sales Navigator export — no scraping
- ❌ **Raw web scraping of personal data** — not worth the risk
- ❌ **Purchased contact lists from shady brokers** — never

**Bottom line:** We can be aggressive on *what signals we detect* while being clean on *how we get the data.* That's actually a selling point: "We do it the right way."

✅ **DECISION (2026-02-26):** Jamie agrees — clean data sourcing only. Licensed APIs + public data. No scraping, no shady brokers. This is a selling point, not a limitation.

---

## Pain Point Signals to Detect (Expanded from Jack's Email)

Based on Jack's ask + what drives MSP sales for SMBs:

### Compliance & Regulatory Signals
1. **HIPAA compliance deadlines** — healthcare/dental offices in MA
2. **PCI-DSS requirements** — any business processing credit cards
3. **CMMC/NIST compliance** — businesses with government contracts
4. **MA Data Privacy Law (201 CMR 17.00)** — requires written info security programs
5. **Cyber insurance requirements tightening** — insurers now demanding MFA, EDR, backups
6. **Industry-specific audits** (SOX for finance, FERPA for education)

### Growth & Change Signals
7. **Hiring surges** — 5+ job postings = growing, likely outgrowing IT
8. **Office relocation/expansion** — new lease filings, address changes
9. **Funding rounds** (for startups in the area)
10. **M&A activity** — acquisitions = IT integration headaches
11. **New business registrations** — MA Secretary of State filings
12. **Leadership changes** — new CEO/CFO often triggers vendor review

### Pain/Risk Signals
13. **Job posting for IT Manager/IT Director** — they're trying to hire in-house = perfect MSP pitch ("why hire one person when you get a whole team?")
14. **Negative Glassdoor/Indeed reviews mentioning IT issues**
15. **Website security issues** — expired SSL, outdated CMS, no HTTPS
16. **Data breach history** — public breach notifications (MA AG publishes these)
17. **Technology stack age** — companies running Windows 10 after EOL (Oct 2025), old server hardware
18. **Vendor transitions** — businesses leaving other MSPs (review sites, forums)

### Timing Signals
19. **Contract renewal cycles** — most MSP contracts are annual, Jan/Jul renewals common
20. **Budget season** — Q4 planning, Q1 spending
21. **Fiscal year alignment** — government/education follow different cycles
22. **Seasonal demand** — tax season (accounting firms), enrollment (schools), open enrollment (healthcare)

→ **Prioritize with Jack on-site: which 5-10 signals matter most?**

---

## Security Requirements (Non-Negotiable)

### Application Security
- HTTPS everywhere (TLS 1.3)
- Authentication via OAuth2/OIDC (Clerk or Auth0)
- Role-based access control (admin vs. viewer)
- Rate limiting on all API endpoints
- Input validation and parameterized queries (no SQL injection)
- Content Security Policy headers
- CORS locked to known origins only

### Data Security
- PostgreSQL with encryption at rest
- All prospect PII encrypted in database
- API keys and secrets in AWS Secrets Manager (never in code, never in .env committed to git)
- No prospect data in application logs
- Data retention policy: 12 months, then anonymize or purge

### Infrastructure
- Hosted on AWS/GCP (SOC 2 compliant)
- Docker containers with minimal base images (Alpine)
- Automated dependency scanning (Snyk/Dependabot)
- No default credentials anywhere
- VPC with private subnets for database
- WAF in front of the web app

### Audit & Monitoring
- Structured logging (who accessed what, when)
- Alerting on anomalous access patterns
- Monthly dependency updates
- Penetration test before launch (even basic automated scan)

---

## Architecture (High-Level)

```
[Signal Sources]                    [User Interface]
  ├─ Job Boards API                    ├─ Prospect Dashboard
  ├─ Business Registrations            ├─ Signal Feed (daily)
  ├─ News/Press (RSS + scrape)         ├─ Prospect Profiles
  ├─ Compliance Databases              ├─ Outreach Recommendations
  ├─ Apollo/ZoomInfo (enrichment)      └─ Export / CRM Push
  ├─ Google Maps / Yelp
  └─ Website Tech Detection
         ↓
[Signal Ingestion Pipeline (daily cron)]
         ↓
[AI Scoring Engine]
  - Match signals to ICP
  - Score urgency (1-100)
  - Generate approach angle / talk track
  - Rank top 25 prospects
         ↓
[Prospect Database (PostgreSQL, encrypted)]
         ↓
[API Layer (FastAPI)]
         ↓
[Web App (React/Next.js)]
```

### Tech Stack (Proposed)
- **Frontend:** Next.js (React) + Tailwind CSS
- **Backend:** Python FastAPI
- **Database:** PostgreSQL (Supabase or AWS RDS)
- **AI/LLM:** OpenAI GPT-4 or Claude for signal analysis + approach angle generation
- **Signal Ingestion:** Python workers on cron (daily)
- **Enrichment:** Apollo.io or ZoomInfo API
- **Tech Detection:** BuiltWith API or Wappalyzer
- **Job Postings:** Indeed API, LinkedIn Jobs API, or scraped job boards
- **Business Data:** MA Secretary of State API, Google Places API
- **Auth:** Clerk
- **Hosting:** Vercel (frontend) + AWS Lambda or EC2 (backend)
- **Monitoring:** Sentry + CloudWatch

---

## Third-Party API Cost Options (Q20)

| Service | What It Does | Cost | Notes |
|---------|-------------|------|-------|
| Apollo.io | Contact enrichment + prospecting | Free tier: 10K credits/mo. Pro: $49/mo | Best bang for buck |
| ZoomInfo | Enterprise contact + company data | $15K+/yr | Overkill for now |
| Clearbit | Company enrichment | $99/mo+ | Good for company-level signals |
| Crunchbase | Funding/M&A data | $29/mo (basic) | Good for startup signals |
| BuiltWith | Tech stack detection | $295/mo | Identifies outdated tech |
| Google Places API | Business verification | $0.017/request | Cheap, essential |
| OpenAI API | Signal analysis + approach gen | ~$50-200/mo | Depends on volume |
| SendGrid/Mailgun | Email if we integrate outreach | Free tier available | For Project 1 overlap |
| Twilio | SMS/Voice | Pay per use | For Project 1 overlap |

**Recommended starter stack:** Apollo.io (free tier) + Crunchbase ($29) + Google Places + OpenAI = **~$100-150/mo** to start. Scale up as revenue proves out.

✅ **DECISION (2026-02-26):** Going with starter stack. No ZoomInfo or premium tiers until revenue justifies it.

---

## Phases

### Phase 1: ICP + Signal Pipeline (Week 1-2)
- Finalize ICP with Jay/Jack
- Build signal ingestion for top 5 signals
- Set up database + enrichment pipeline
- Daily cron for signal collection

### Phase 2: Scoring + UI (Week 2-4)
- Build AI scoring engine (match signals to ICP, rank prospects)
- Build web dashboard (prospect list, signal feed, profiles)
- Generate AI-written approach angles for each prospect
- Auth + RBAC for Jack + Jamie

### Phase 3: Launch + Iterate (Week 4-6)
- Deploy to production
- Jack + Jamie use daily for 2 weeks
- Collect feedback, tune scoring, add signals
- Measure: meetings booked from engine-sourced prospects

### Phase 4: Scale (Month 2+)
- Roll out to full Cinch IT sales team
- Add more signal sources
- Integrate with ConnectWise (push prospects into their pipeline)
- Build reporting (ROI dashboard)

---

## Questions for On-Site Meeting with Jay/Jack
→ See: `../onsite-discovery-questions.md`
