# Cinch IT Reactivation - Task List

**Priority System:** 🚨 Critical | 🔥 High | 📋 Medium | 💡 Nice-to-have

---

## 🚨 CRITICAL - Launch Blockers (Do First)

### Backend Setup (MoneyMachine)
- [ ] Buy getcinchmsp.com domain
- [ ] Sign up SendGrid + configure domain authentication  
- [ ] Sign up Twilio + get SMS-capable phone number
- [ ] Sign up Apollo.io for contact enrichment
- [ ] Configure all API keys in .env file
- [ ] Initialize database + import 644 contacts
- [ ] Test SMS sending to Jamie's number

### Frontend Foundation (Jamie - Claude Pro)
- [ ] **Dashboard Homepage** - Main stats, recent activity, quick actions
  - SMS/Email metrics (sent, replies, meetings booked)
  - Recent contact responses
  - Quick SMS/Email send buttons
  - Contact status breakdown (Ready/Needs Enrichment/DNC)
- [ ] **Contact List View** - Table with search, filters, pagination
  - Sortable columns (Name, Company, Last Activity, Status, SMS Consent)
  - Bulk action checkboxes
  - Filter by: Status, SMS consent, Last outreach date
  - Search by: Name, company, email, phone

---

## 🔥 HIGH PRIORITY - Core Features

### Jamie (Frontend Focus)
- [ ] **Contact Detail View** - Individual contact profile
  - Contact info + enrichment data (Apollo results)
  - Outreach history timeline (SMS/Email events)
  - Quick send SMS/Email forms
  - Manual notes section
  - Status change buttons (Ready → DNC, etc.)
- [ ] **SMS Campaign Builder** - Create/edit SMS sequences
  - Template editor with {first_name}, {company} variables  
  - Preview SMS with real contact data
  - Sequence timing controls (delay between steps)
  - A/B test different message versions
- [ ] **Outreach Queue** - Pending and scheduled messages
  - Today's outreach list
  - Schedule upcoming SMS blasts
  - Pause/resume campaigns
  - Test mode toggle (send to Jamie only)

### MoneyMachine (Backend Support)
- [ ] **Real-time webhook handling** - Twilio SMS replies, SendGrid events
- [ ] **Background job scheduler** - Automated sequence sending
- [ ] **Response classification** - AI categorization of replies
- [ ] **Meeting booking integration** - Calendly/Cal.com connection

---

## 📋 MEDIUM PRIORITY - Growth Features  

### Jamie (Frontend)
- [ ] **Analytics Dashboard** - Campaign performance metrics
  - Response rate trends over time
  - SMS vs Email performance comparison
  - Contact source analysis (which segments convert best)
  - Revenue attribution (contacts → meetings → deals)
- [ ] **Bulk Actions** - Multi-contact operations
  - Bulk SMS send (with safety confirmations)
  - Bulk status updates (Mark as DNC, etc.)
  - Export contact lists
  - Import new contact batches

### MoneyMachine (Backend)
- [ ] **Advanced enrichment** - Apollo + Google Places integration
- [ ] **Sequence optimization** - Auto-pause low-performing sequences
- [ ] **Lead scoring** - AI-powered lead quality assessment
- [ ] **CRM integration** - Sync with Cinch IT's existing systems

---

## 💡 NICE-TO-HAVE - Polish & Optimization

- [ ] **Mobile responsiveness** - Works on phone/tablet
- [ ] **Dark mode toggle** - Theme switcher
- [ ] **Advanced filtering** - Date ranges, custom segments
- [ ] **Automated reporting** - Weekly SMS performance emails
- [ ] **Voice calling integration** - AI voice outreach (Bland.ai)
- [ ] **Multi-user support** - Team access controls

---

## 🔗 Handoff Points (Check HANDOFF.md)

**When Jamie needs MoneyMachine:**
1. New API endpoints for frontend features
2. Database schema changes
3. External service integrations (Twilio, SendGrid)
4. Background job logic
5. Production deployment

**When MoneyMachine needs Jamie:**
1. Frontend design decisions
2. UI/UX feedback
3. User workflow validation
4. Component integration testing

---

## 🎯 Sprint Planning

**Sprint 1 (This Week):** Dashboard + Contact List → Get something visual working
**Sprint 2:** Contact Detail + SMS sending → Core functionality  
**Sprint 3:** Campaign Builder → Sequence management
**Sprint 4:** Analytics + Polish → Production ready

**Deadline:** March 15th for first SMS campaigns to go live (domain warmup needed)