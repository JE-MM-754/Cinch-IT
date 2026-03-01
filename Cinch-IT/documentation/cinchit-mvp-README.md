# CinchIT MVP - Prospect Management Tool

**A simple, fast prospect management system for IT service providers**

Built for Jack Wilson (Cinch IT franchisee) to manage and score IT service prospects effectively.

## 🚀 Features

- **Prospect Management**: Add, edit, delete, and organize IT service prospects
- **Scoring System**: Manual 1-100 scoring for prospect prioritization  
- **Dashboard**: Clean interface to view prospects sorted by score
- **Export**: CSV export functionality for external tools
- **Search & Filter**: Find prospects by status, score, or company details
- **Statistics**: Dashboard with prospect counts, average scores, and top prospects

## 🏗️ Tech Stack

**Backend:**
- **FastAPI** - Modern, fast Python web framework
- **SQLite** - Lightweight database (no complex PostgreSQL setup)
- **Pydantic** - Data validation and serialization

**Frontend:**
- **Vanilla HTML/CSS/JavaScript** - No complex frameworks
- **Static files** served by FastAPI
- **Responsive design** for desktop and mobile

## 🎯 Design Philosophy

**Keep it Simple:** This is an MVP focused on core functionality that Jack can start using immediately. Complex features like AI scoring, authentication, and external APIs can be added later.

**Fast Development:** Built in ~3 hours vs. 20+ hours for enterprise solutions.

**Production Ready:** Includes proper error handling, data validation, and professional UI.

## 📋 Installation & Setup

### Prerequisites
- Python 3.9+
- pip

### Quick Start

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd cinchit-mvp
   ```

2. **Install dependencies:**
   ```bash
   pip install fastapi uvicorn
   ```

3. **Run the application:**
   ```bash
   uvicorn main:app --reload
   ```

4. **Open your browser:**
   ```
   http://localhost:8000
   ```

The database will be automatically created on first run.

## 📊 API Endpoints

### Prospects
- `GET /api/prospects` - List all prospects (with sorting and filtering)
- `GET /api/prospects/{id}` - Get specific prospect
- `POST /api/prospects` - Create new prospect  
- `PUT /api/prospects/{id}` - Update prospect
- `DELETE /api/prospects/{id}` - Delete prospect

### Analytics
- `GET /api/stats` - Get dashboard statistics
- `GET /api/export/csv` - Export prospects to CSV

### Frontend
- `GET /` - Serve main dashboard interface
- `GET /static/*` - Serve static assets

## 💾 Database Schema

**Prospects Table:**
```sql
CREATE TABLE prospects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_name TEXT NOT NULL,
    contact_name TEXT NOT NULL DEFAULT '',
    contact_email TEXT NOT NULL DEFAULT '',
    contact_phone TEXT NOT NULL DEFAULT '',
    industry TEXT NOT NULL DEFAULT '',
    employee_count INTEGER DEFAULT 0,
    score INTEGER NOT NULL DEFAULT 50 CHECK(score >= 1 AND score <= 100),
    status TEXT NOT NULL DEFAULT 'new' CHECK(status IN ('new', 'contacted', 'qualified', 'proposal', 'won', 'lost')),
    notes TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
)
```

## 🎨 UI Features

- **Prospect List**: Sortable table with all prospect information
- **Add/Edit Forms**: Clean forms for prospect data entry
- **Dashboard Stats**: Key metrics and top prospects
- **Status Management**: Track prospect progression through sales pipeline
- **Responsive Design**: Works on desktop and mobile devices
- **Export Function**: One-click CSV export for external analysis

## 📈 Scoring System

**Manual Scoring (1-100):**
- **90-100**: Hot prospects (immediate follow-up)
- **70-89**: Qualified leads (active pursuit)  
- **50-69**: Potential prospects (nurture)
- **30-49**: Long-term opportunities
- **1-29**: Low-priority or poor fit

*Future versions will include AI-powered scoring based on signals like hiring activity, IT job postings, and company growth indicators.*

## 🔄 Status Pipeline

- **New**: Initial prospect entry
- **Contacted**: First outreach completed
- **Qualified**: Confirmed need and budget
- **Proposal**: Proposal sent
- **Won**: Deal closed successfully  
- **Lost**: Opportunity lost

## 🚀 Future Enhancements

**Phase 2 Features (Planned):**
- AI-powered scoring using Claude Haiku
- Signal detection (hiring surges, IT roles, compliance deadlines)
- Authentication and user management
- Advanced filtering and search
- Integration with Apollo.io, Crunchbase APIs
- Email marketing integration
- Pipeline analytics and reporting

## 🏢 Business Context

**Target User:** Jack Wilson, Cinch IT franchisee  
**Use Case:** Daily prospect management for IT service sales  
**Goal:** Simple tool to organize, score, and track IT service prospects

**Competitive Advantage:** Unlike generic CRM systems, this is purpose-built for IT service providers with scoring optimized for SMB IT needs.

## 📝 Development Notes

**Architecture Decision:** Started with simplest possible stack to get Jack a working tool immediately. Complex enterprise features (PostgreSQL, authentication, AI) deliberately excluded from MVP.

**Build Time:** ~3 hours (vs. 20+ hours for full enterprise version)

**Code Quality:** Production-ready with proper error handling, data validation, and security considerations within the simple scope.

## 🔗 Related Projects

- **CinchIT AI Engine**: Enterprise version with AI scoring, external APIs, and advanced features
- **Gaming Build Research**: Research methodology for specialized optimization

## 📞 Support

For questions or enhancements, contact the development team.

---

**Built with ❤️ for effective IT service prospect management**