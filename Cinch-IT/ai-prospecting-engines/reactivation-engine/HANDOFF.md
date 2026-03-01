# Integration Handoff Points

**Clear division between Frontend (Jamie) and Backend (MoneyMachine)**

---

## 🔄 Workflow

1. **Jamie builds UI components** using Claude Pro/Cursor
2. **Commits to GitHub** with screenshots/demos  
3. **MoneyMachine reviews** via `git pull` + screenshots
4. **MoneyMachine handles** API integration + backend logic
5. **Repeat** for next component

---

## 📋 Current Backend API (Ready to Use)

**Base URL:** `http://localhost:8000/api`

### Dashboard Data
```
GET /dashboard/stats
Returns: contacts{total, ready, sms_ready, email_only}, outreach{sms_sent, sms_replies, email_sent, etc}
```

### Contact Management  
```
GET /contacts?status=ready&search=company&page=1&per_page=50
GET /contacts/{id} 
PATCH /contacts/{id} - Update status, notes, consent flags
```

### Outreach
```
POST /outreach/send-sms/{contact_id} - Send single SMS
POST /outreach/send-test-sms - Test SMS to Jamie's number
POST /outreach/start-sms-blitz?limit=10 - Bulk SMS send
GET /outreach/events?channel=sms&status=sent - Outreach history
```

### Sequences
```
GET /sequences - List available SMS/email sequences  
POST /sequences/init-sms-first - Initialize SMS-first templates
```

---

## 🔴 Handoff Triggers (When Jamie Calls MoneyMachine)

### 1. "I need a new API endpoint"
**Jamie commits:** Frontend code that calls non-existent endpoint
**MoneyMachine builds:** Backend endpoint + database logic
**Example:** Contact bulk update, advanced filtering, export features

### 2. "The API response doesn't have what I need"  
**Jamie screenshots:** UI mockup showing required data
**MoneyMachine updates:** API response format + database queries
**Example:** Contact list needs last outreach date, response classification

### 3. "I'm getting errors when testing"
**Jamie provides:** Error messages, browser console logs
**MoneyMachine debugs:** API issues, CORS problems, data validation
**Example:** SMS sending fails, contact updates don't persist

### 4. "I built the UI, how do I connect it?"
**Jamie demos:** Working UI components (screenshots/video)
**MoneyMachine integrates:** Hook up frontend to backend APIs
**Example:** Campaign builder UI → sequence creation API

---

## ✅ Self-Service (Jamie Handles Alone)

- **UI Layout & Styling** - Components, CSS, responsive design
- **Form Validation** - Client-side input checking, UX feedback  
- **State Management** - React state, data flow between components
- **Navigation** - Routing between pages, breadcrumbs
- **Basic API Calls** - GET/POST to existing endpoints (documented above)

---

## 🚨 Always MoneyMachine (Never Jamie)

- **Database Schema** - New tables, columns, indexes, migrations  
- **External APIs** - Twilio, SendGrid, Apollo integration
- **Background Jobs** - Scheduled SMS sending, webhook processing
- **Security** - Authentication, authorization, data protection
- **Production Deployment** - Server setup, domain configuration

---

## 📸 Review Process

### Jamie → MoneyMachine Handoff
1. **Commit code** to GitHub with descriptive message
2. **Screenshot** the working UI (before/after if updating)
3. **List integration needs** - "This needs to save to database", "This needs real contact data"
4. **Tag issues** - Create GitHub issues for backend work needed

### MoneyMachine → Jamie Feedback  
1. **Test integration** - Verify frontend connects to new backend
2. **Suggest improvements** - UX, data flow, performance optimizations  
3. **Update documentation** - New API endpoints, changed response formats
4. **Mark ready** - Component fully integrated and tested

---

## 🚀 Communication Channels

**For quick questions:** Discord/chat
**For detailed issues:** GitHub issues with screenshots  
**For planning:** Weekly check-ins via war room
**For demos:** Screen recordings or live demos

---

## 📁 File Organization

```
/frontend/
  /src/
    /components/     # Reusable UI components (Jamie)
    /pages/         # Route pages (Jamie)  
    /hooks/         # Custom React hooks (Jamie)
    /api/           # API integration layer (Shared)
    /types/         # TypeScript definitions (MoneyMachine)
  /public/          # Static assets (Jamie)

/backend/           # All backend code (MoneyMachine)
/docs/             # API documentation (MoneyMachine)
```

**Rule:** Jamie owns `/frontend/src/components|pages|hooks`, MoneyMachine handles everything else + integration.