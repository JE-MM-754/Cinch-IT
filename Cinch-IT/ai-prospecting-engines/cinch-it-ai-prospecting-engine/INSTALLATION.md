# Installation Guide - Cinch IT AI Prospecting Engine

This guide will help you set up the Cinch IT AI Prospecting Engine on your local development environment.

## Prerequisites

- **Python 3.9+** (recommended: 3.11)
- **Node.js 18+** (for frontend)
- **PostgreSQL 14+**
- **Redis 6+** (for caching and job queues)
- **Docker & Docker Compose** (optional but recommended)

## Quick Start with Docker

The fastest way to get started is using Docker:

```bash
# Clone the repository
git clone https://github.com/cinchit/ai-prospecting-engine.git
cd ai-prospecting-engine

# Copy environment configuration
cp .env.example .env

# Edit the .env file with your API keys and configuration
nano .env

# Start all services with Docker Compose
docker-compose up -d

# Run database migrations
docker-compose exec api python -m alembic upgrade head

# Access the application
# - Frontend: http://localhost:3000
# - API: http://localhost:8000
# - Admin Panel: http://localhost:8000/admin
```

## Manual Installation

### Backend Setup

1. **Create Python virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install Python dependencies:**
```bash
cd ai-engine
pip install -r requirements.txt
```

3. **Set up PostgreSQL database:**
```bash
# Create database
createdb cinch_it_prospecting

# Run migrations
python -m alembic upgrade head

# Seed initial data (optional)
python scripts/seed_data.py
```

4. **Configure environment variables:**
```bash
cp .env.example .env
```

Edit `.env` with your configuration:
```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/cinch_it_prospecting

# AI Services
OPENAI_API_KEY=sk-your-openai-api-key
ANTHROPIC_API_KEY=your-anthropic-api-key

# Web Scraping
SCRAPERAPI_KEY=your-scraperapi-key
BRIGHT_DATA_KEY=your-bright-data-key

# Outreach
SENDGRID_API_KEY=your-sendgrid-api-key
LINKEDIN_API_TOKEN=your-linkedin-token

# External Services
APOLLO_API_KEY=your-apollo-api-key
CLEARBIT_API_KEY=your-clearbit-api-key
```

5. **Start the backend server:**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

1. **Install Node.js dependencies:**
```bash
cd frontend
npm install
```

2. **Configure frontend environment:**
```bash
cp .env.local.example .env.local
```

Edit `.env.local`:
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

3. **Start the development server:**
```bash
npm run dev
```

### Redis Setup

1. **Install and start Redis:**
```bash
# macOS with Homebrew
brew install redis
brew services start redis

# Ubuntu/Debian
sudo apt-get install redis-server
sudo systemctl start redis-server

# Docker
docker run -d -p 6379:6379 --name redis redis:alpine
```

2. **Start background workers:**
```bash
cd ai-engine
celery -A worker.celery worker --loglevel=info

# In separate terminal - start scheduler
celery -A worker.celery beat --loglevel=info
```

## Configuration

### AI Engine Configuration

The AI engine requires several API keys for optimal performance:

1. **OpenAI API Key** - For natural language processing and lead analysis
2. **Anthropic API Key** - For strategic analysis and content generation  
3. **Apollo API Key** - For contact enrichment and validation
4. **Clearbit API Key** - For company intelligence gathering

### Data Collection Setup

1. **Web Scraping Configuration:**
   - Configure rate limiting in `scraper/config.py`
   - Set up proxy rotation for large-scale operations
   - Adjust scraping intervals based on source requirements

2. **LinkedIn Integration:**
   - Obtain LinkedIn API credentials through LinkedIn Developer Program
   - Configure automation limits to comply with LinkedIn ToS
   - Set up connection request templates

### Outreach Configuration

1. **Email Templates:**
   - Customize templates in `templates/email/`
   - Configure A/B testing scenarios
   - Set up drip campaign sequences

2. **CRM Integration:**
   - Configure HubSpot or Salesforce credentials
   - Map lead fields to CRM properties
   - Set up automatic lead scoring

## Development Workflow

### Running Tests

```bash
# Backend tests
cd ai-engine
python -m pytest tests/ -v

# Frontend tests  
cd frontend
npm run test

# E2E tests
npm run test:e2e
```

### Code Quality

```bash
# Backend linting
cd ai-engine
black . && isort . && flake8 .

# Frontend linting
cd frontend
npm run lint && npm run type-check
```

### Database Migrations

```bash
# Create new migration
cd ai-engine
python -m alembic revision --autogenerate -m "Description of changes"

# Apply migration
python -m alembic upgrade head

# Rollback migration
python -m alembic downgrade -1
```

## Production Deployment

### Using Docker Compose

```bash
# Build production images
docker-compose -f docker-compose.prod.yml build

# Deploy with environment variables
ENVIRONMENT=production docker-compose -f docker-compose.prod.yml up -d

# Run database migrations
docker-compose -f docker-compose.prod.yml exec api python -m alembic upgrade head
```

### Environment Variables for Production

```bash
# Security
SECRET_KEY=your-super-secret-key
CORS_ORIGINS=https://yourdomain.com

# Database
DATABASE_URL=postgresql://user:password@db-host:5432/cinch_it_prospecting

# Redis
REDIS_URL=redis://redis-host:6379/0

# Monitoring
SENTRY_DSN=your-sentry-dsn
```

### SSL and Domain Setup

1. **Configure reverse proxy** (nginx recommended)
2. **Set up SSL certificates** (Let's Encrypt recommended)
3. **Configure domain DNS** to point to your server
4. **Set up monitoring** with health checks

## Troubleshooting

### Common Issues

1. **Database connection errors:**
   - Verify PostgreSQL is running
   - Check database URL and credentials
   - Ensure database exists and migrations are applied

2. **API key failures:**
   - Verify all required API keys are set
   - Check API key permissions and rate limits
   - Monitor API usage dashboards

3. **Scraping failures:**
   - Check proxy configuration and rotation
   - Verify rate limiting settings
   - Monitor for IP blocking

4. **Memory issues:**
   - Increase worker memory limits
   - Optimize data processing batch sizes
   - Configure proper garbage collection

### Performance Optimization

1. **Database optimization:**
   - Add appropriate indexes
   - Configure connection pooling
   - Monitor slow queries

2. **Caching strategy:**
   - Configure Redis cache TTLs
   - Implement cache warming
   - Monitor cache hit rates

3. **Background job optimization:**
   - Configure optimal worker count
   - Implement job prioritization
   - Monitor job queue lengths

## Support

For technical support and questions:

- **Documentation:** Check the `/docs` directory for detailed technical documentation
- **Issues:** Report bugs via GitHub Issues
- **Discord:** Join our developer community
- **Email:** support@cinchit.com for enterprise support

## Security Considerations

- **API Keys:** Store in environment variables, never commit to version control
- **Database:** Use strong passwords and enable SSL connections
- **Rate Limiting:** Configure appropriate limits to avoid service abuse
- **GDPR Compliance:** Ensure data collection complies with privacy regulations

---

**Next Steps:** After installation, see [USAGE.md](USAGE.md) for operational guidance and [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for integration details.