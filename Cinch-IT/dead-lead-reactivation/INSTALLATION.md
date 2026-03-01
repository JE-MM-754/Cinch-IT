# Installation Guide - Cinch IT Dead Lead Reactivation

This guide will help you set up the Dead Lead Reactivation system for SMS-first outreach campaigns.

## Prerequisites

- **Python 3.9+** (recommended: 3.11)
- **Node.js 18+** (for frontend)
- **PostgreSQL 14+**
- **Redis 6+** (for background jobs)
- **Twilio Account** (for SMS)
- **SendGrid Account** (for email)

## Quick Start

```bash
# Clone the repository
git clone https://github.com/cinchit/dead-lead-reactivation.git
cd dead-lead-reactivation

# Set up environment
cp .env.example .env
# Edit .env with your API keys

# Start with Docker (recommended)
docker-compose up -d

# Or install manually (see below)
```

## Docker Installation (Recommended)

### Prerequisites
- Docker Desktop or Docker Engine
- Docker Compose v2+

### Setup Steps

1. **Clone and configure:**
```bash
git clone https://github.com/cinchit/dead-lead-reactivation.git
cd dead-lead-reactivation
cp .env.example .env
```

2. **Edit environment variables:**
```bash
nano .env
```

Required configuration:
```bash
# Database
DATABASE_URL=postgresql://postgres:password@db:5432/dead_leads

# SMS Service (Twilio)
TWILIO_ACCOUNT_SID=your-twilio-account-sid
TWILIO_AUTH_TOKEN=your-twilio-auth-token
TWILIO_PHONE_NUMBER=+1234567890

# Email Service (SendGrid)
SENDGRID_API_KEY=your-sendgrid-api-key
SENDGRID_FROM_EMAIL=your-verified-email@domain.com

# AI Analysis
OPENAI_API_KEY=sk-your-openai-api-key

# Contact Enrichment
APOLLO_API_KEY=your-apollo-api-key
```

3. **Start all services:**
```bash
docker-compose up -d
```

4. **Initialize database:**
```bash
# Run migrations
docker-compose exec backend python -m alembic upgrade head

# Import your lead data
docker-compose exec backend python scripts/import_leads.py data/leads.csv
```

5. **Access the application:**
- **Frontend:** http://localhost:3000
- **API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

## Manual Installation

### Backend Setup

1. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

2. **Install dependencies:**
```bash
cd backend
pip install -r requirements.txt
```

3. **Set up PostgreSQL:**
```bash
# Create database
createdb dead_leads

# Set database URL in .env
DATABASE_URL=postgresql://user:password@localhost:5432/dead_leads
```

4. **Run database migrations:**
```bash
python -m alembic upgrade head
```

5. **Start the API server:**
```bash
uvicorn main:app --reload --port 8000
```

### Frontend Setup

1. **Install Node.js dependencies:**
```bash
cd frontend
npm install
```

2. **Configure environment:**
```bash
cp .env.local.example .env.local
```

Edit `.env.local`:
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

3. **Start development server:**
```bash
npm run dev
```

### Background Workers

1. **Start Redis:**
```bash
# macOS
brew install redis && brew services start redis

# Ubuntu
sudo apt install redis-server && sudo systemctl start redis

# Docker
docker run -d -p 6379:6379 redis:alpine
```

2. **Start background workers:**
```bash
cd backend
python -m celery -A worker.app worker --loglevel=info
```

## Configuration

### SMS Configuration (Twilio)

1. **Get Twilio credentials:**
   - Sign up at [twilio.com](https://twilio.com)
   - Get Account SID and Auth Token from Console
   - Purchase a phone number for SMS

2. **Configure compliance:**
```python
# In backend/services/sms.py
SMS_COMPLIANCE = {
    "opt_out_keywords": ["STOP", "UNSUBSCRIBE", "QUIT"],
    "rate_limit": 1,  # messages per second
    "business_hours": (9, 17),  # 9 AM to 5 PM
    "timezone": "US/Eastern"
}
```

3. **Set up webhook for replies:**
```bash
# Twilio webhook URL (replace with your domain)
https://yourdomain.com/api/sms/webhook
```

### Email Configuration (SendGrid)

1. **Get SendGrid API key:**
   - Sign up at [sendgrid.com](https://sendgrid.com)
   - Create API key with full access
   - Verify sender email address

2. **Configure templates:**
```bash
# Templates stored in backend/templates/email/
├── introduction.html
├── follow_up.html
├── value_proposition.html
└── meeting_request.html
```

### AI Configuration

1. **OpenAI setup:**
```bash
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-4  # or gpt-3.5-turbo for cost savings
```

2. **Response classification prompts:**
```python
# In backend/services/ai_classifier.py
CLASSIFICATION_PROMPTS = {
    "interested": "Positive response indicating interest in services",
    "not_interested": "Clear rejection or no interest",
    "request_info": "Asking for more information",
    "timing": "Interest but not ready now",
    "budget": "Price or budget concerns"
}
```

## Data Import

### Preparing Lead Data

Your CSV should have these columns:
```csv
company_name,contact_name,phone,email,last_contact_date,notes,source
Acme Corp,John Doe,+15551234567,john@acme.com,2023-06-15,Interested but no budget,website
```

### Import Process

1. **Validate data format:**
```bash
cd backend
python scripts/validate_leads.py data/leads.csv
```

2. **Import leads:**
```bash
python scripts/import_leads.py data/leads.csv --batch-size 100
```

3. **Enrich missing data:**
```bash
python scripts/enrich_contacts.py --phone-only
```

## Campaign Setup

### Creating SMS Campaigns

1. **Access the dashboard:** http://localhost:3000/campaigns

2. **Create new campaign:**
   - Choose lead segment (phone available, last contact > 6 months)
   - Select message template or create custom
   - Set schedule and rate limits
   - Enable compliance features

3. **Campaign templates:**
```json
{
  "name": "Q1 Reactivation",
  "message_sequence": [
    {
      "delay_hours": 0,
      "template": "introduction",
      "personalize": true
    },
    {
      "delay_hours": 72,
      "template": "follow_up",
      "condition": "no_response"
    }
  ],
  "rate_limit": "10/hour",
  "business_hours_only": true
}
```

### Monitoring and Analytics

1. **Real-time dashboard:**
   - Message delivery rates
   - Response rates by template
   - Conversion tracking
   - Compliance monitoring

2. **Export results:**
```bash
# Generate campaign report
python scripts/generate_report.py --campaign-id 123 --format csv
```

## Testing

### Development Testing

```bash
# Backend tests
cd backend
python -m pytest tests/ -v

# Frontend tests
cd frontend  
npm test

# Integration tests
python -m pytest tests/integration/ -v
```

### SMS Testing

1. **Test mode configuration:**
```bash
# In .env
SMS_TEST_MODE=true
SMS_TEST_PHONE=+15551234567  # Your phone for testing
```

2. **Test message flow:**
```bash
# Send test message
curl -X POST http://localhost:8000/api/campaigns/test \
  -H "Content-Type: application/json" \
  -d '{"phone": "+15551234567", "template": "introduction"}'
```

## Production Deployment

### Environment Configuration

```bash
# Production .env
ENVIRONMENT=production
DEBUG=false
SECRET_KEY=your-super-secret-production-key

# Database (managed service recommended)
DATABASE_URL=postgresql://user:pass@prod-db:5432/dead_leads

# Redis (managed service recommended)
REDIS_URL=redis://prod-redis:6379/0

# Monitoring
SENTRY_DSN=your-sentry-dsn
```

### Deployment Options

1. **Docker Compose (simple):**
```bash
docker-compose -f docker-compose.prod.yml up -d
```

2. **Kubernetes (scalable):**
```bash
kubectl apply -f k8s/
```

3. **Platform as a Service:**
   - Heroku with add-ons
   - Railway or Render
   - DigitalOcean App Platform

### Monitoring Setup

1. **Health checks:**
```bash
# API health
curl http://localhost:8000/health

# Database connection
curl http://localhost:8000/health/db

# SMS service status
curl http://localhost:8000/health/sms
```

2. **Logging configuration:**
```python
# In backend/core/logging.py
LOGGING = {
    "version": 1,
    "handlers": {
        "file": {
            "filename": "logs/app.log",
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5
        }
    }
}
```

## Compliance & Legal

### TCPA Compliance

- **Opt-in consent:** Ensure all contacts have opted in for SMS
- **Easy opt-out:** Include "Reply STOP to opt out" in messages
- **Time restrictions:** Only send during business hours
- **Rate limiting:** Respect carrier limits and best practices

### Data Privacy

- **Encryption:** All PII encrypted at rest and in transit
- **Access controls:** Role-based access to sensitive data
- **Audit logging:** Track all data access and modifications
- **Data retention:** Automatic cleanup of old campaign data

## Troubleshooting

### Common Issues

1. **SMS delivery failures:**
   - Check Twilio account balance
   - Verify phone number format (+1XXXXXXXXXX)
   - Check carrier filtering/blocking

2. **Database connection errors:**
   - Verify PostgreSQL is running
   - Check connection string format
   - Ensure database exists

3. **High response processing delays:**
   - Scale Redis workers
   - Optimize AI classification prompts
   - Check OpenAI API rate limits

### Performance Optimization

1. **Database indexing:**
```sql
CREATE INDEX idx_contacts_phone ON contacts(phone);
CREATE INDEX idx_messages_campaign_id ON messages(campaign_id);
CREATE INDEX idx_messages_created_at ON messages(created_at);
```

2. **Redis optimization:**
```bash
# Increase memory limit
redis-server --maxmemory 1gb --maxmemory-policy allkeys-lru
```

## Support

- **Documentation:** `/docs` directory for detailed API docs
- **GitHub Issues:** Report bugs and feature requests  
- **Email:** support@cinchit.com for urgent issues
- **Discord:** Join our developer community

---

**Next Steps:** See [USAGE.md](USAGE.md) for campaign management and [API.md](API.md) for integration details.