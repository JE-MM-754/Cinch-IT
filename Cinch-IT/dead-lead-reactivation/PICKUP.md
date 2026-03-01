# DEVELOPMENT PICKUP - 2026-03-01

## CURRENT STATE
- **Last worked by:** Claude Code QA Pass
- **Branch:** main
- **Status:** Backend running, Frontend wired to real backend data

## WHAT'S WORKING

### Backend (100% functional for local dev)
- FastAPI on localhost:8000 with all 19 endpoints
- SQLite database with 644 real contacts imported from CSV
- 3 SMS-first sequences initialized
- Audit log tracking all actions
- Test mode ON by default (no accidental outreach)
- API proxy from frontend :3000 to backend :8000 working

### Frontend (Reactivation module fully wired)
- Next.js 16 on localhost:3000, all 14 routes return 200
- Build passes clean (zero TypeScript errors)
- **Reactivation Dashboard** fetches real stats from /api/dashboard/stats
- **Contacts page** fetches 644 real contacts with pagination, search, and status filter
- **Sequences page** fetches 3 real SMS-first sequences from /api/sequences
- **Audit Log page** fetches real audit trail from /api/audit
- **Home page** shows real contact counts from backend
- Prospecting and Intelligence modules use demo data (no backend equivalent yet)

## WHAT WAS BROKEN (fixed in this QA pass)

1. **Frontend used hardcoded demo data** - Dashboard showed "1,248 dormant contacts" but only had 8 fake records. Now fetches real data from backend API showing 644 actual contacts.
2. **Contacts page showed 8 demo records** - Rewired to fetch from /api/contacts with pagination (20 per page), search by name/company/email, and status filter.
3. **Sequences page showed fake templates** - Now fetches real SMS-first sequences from the backend with step details and channel indicators.
4. **Audit log showed hardcoded events** - Now fetches from /api/audit with real timestamps and details.
5. **Home page stats were fabricated** - Reactivation module card now shows real counts from backend.
6. **At-Risk Deals trend was semantically wrong** - Showed green "up" for a decrease in at-risk deals. Fixed to "down" (negative change).
7. **node_modules were corrupted** - Next.js binary couldn't find its own modules. Cleaned and reinstalled.

## WHAT STILL NEEDS WORK

### High Priority
- **Prospecting module** has no backend API - uses demo data
- **Intelligence module** has no backend API - uses demo data
- **Outreach flow** - "Send SMS" and "Send Email" buttons not yet wired to UI (backend endpoints exist but UI doesn't call them)
- **Contact detail view** - No page to view a single contact's full profile and outreach history
- **Production database** - Currently using SQLite; need PostgreSQL for production

### Medium Priority
- **Action buttons** (Export Segment, Create Sequence, Launch Campaign) are placeholders with no click handlers
- **Charts show demo data** - MonthlyPerformanceChart and PipelineValueChart still use hardcoded monthly performance data
- **No authentication** - Backend has JWT infrastructure but no login UI
- **No real-time updates** - Dashboard doesn't auto-refresh

### Low Priority
- **Accessibility** - Tables missing ARIA attributes and keyboard navigation
- **Input validation** - Search inputs have no sanitization
- **Mobile responsiveness** - Works but could be tighter on small screens

## HOW TO RUN LOCALLY

### Backend
```bash
cd app/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
DATABASE_URL=sqlite:///./cinchit.db python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Then import contacts (one-time):
```bash
curl -X POST http://localhost:8000/api/admin/import-csv
curl -X POST http://localhost:8000/api/sequences/init-sms-first
```

### Frontend
```bash
cd app/frontend
npm install
npm run dev
```

Open http://localhost:3000

### Key URLs
- Frontend: http://localhost:3000
- Backend API docs: http://localhost:8000/docs
- Health check: http://localhost:8000/api/health
- Dashboard stats: http://localhost:8000/api/dashboard/stats

## PRODUCTION DEPLOYMENT NEEDS
- PostgreSQL database (replace SQLite)
- Real API keys in .env (Twilio, SendGrid, OpenAI, Apollo)
- CORS configured for production frontend URL
- SSL/TLS certificates
- Remove test_mode=true from production config
- DNS setup for domain

## TECHNICAL STACK
- **Backend:** FastAPI 0.109.2, SQLAlchemy 2.0.25, Python 3.9+
- **Frontend:** Next.js 16.1.6, React 19, TypeScript 5.9, Tailwind CSS 4
- **Database:** SQLite (dev) / PostgreSQL (prod)
- **Services:** Twilio SMS, SendGrid email, Apollo enrichment, OpenAI classification

## KEY FILES
- `backend/main.py` - 19 REST endpoints
- `backend/config.py` - Environment configuration (test_mode default: true)
- `backend/database.py` - SQLAlchemy engine and session
- `backend/models.py` - 6 database tables
- `backend/services/outreach.py` - SMS/email sending with safety gates
- `frontend/src/app/reactivation/` - 5 pages wired to real backend
- `frontend/src/lib/demo-data.ts` - Demo data for prospecting/intelligence modules
- `frontend/next.config.ts` - API proxy rewrite rule
