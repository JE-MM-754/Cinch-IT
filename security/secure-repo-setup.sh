#!/bin/bash
# Repository Security Setup Script
# Run this on every new repository before Codex/Claude works on it

set -e

REPO_PATH=${1:-.}
cd "$REPO_PATH"

echo "🛡️ Setting up repository security for: $(pwd)"

# 1. Install enhanced .gitignore
echo "📝 Installing secure .gitignore..."
if [ -f .gitignore ]; then
    echo "# Added by OpenClaw Security Setup" >> .gitignore
    echo "" >> .gitignore
fi
cat ~/.openclaw/workspace/security/secure-gitignore-template >> .gitignore
echo "✅ .gitignore updated"

# 2. Install pre-commit hooks
echo "🔧 Setting up pre-commit hooks..."
bash ~/.openclaw/workspace/security/pre-commit-hook-setup.sh
echo "✅ Pre-commit hooks installed"

# 3. Create security documentation
echo "📚 Creating security documentation..."
mkdir -p docs/security
cat > docs/security/README.md << 'EOF'
# Repository Security

This repository has been configured with OpenClaw security safeguards.

## Pre-Commit Protection
- Automatic secret detection before commits
- API key pattern matching
- Dangerous file detection

## Configuration Safety
- All secrets use environment variables
- `.example` files provide templates
- Real credentials never committed

## For Developers
Before working on this repo:
1. Install pre-commit: `pip install pre-commit`
2. Install hooks: `pre-commit install`
3. Test: `pre-commit run --all-files`

## Emergency Procedures
If secrets are accidentally committed:
1. Immediately revoke exposed credentials
2. Contact security team
3. Follow incident response procedures
EOF

# 4. Create environment template
echo "🔧 Creating environment template..."
cat > .env.example << 'EOF'
# Environment Variables Template
# Copy to .env and fill with real values (never commit .env)

# AI API Keys
ANTHROPIC_API_KEY=sk-ant-your-key-here
OPENAI_API_KEY=sk-proj-your-key-here

# OpenClaw
OPENCLAW_GATEWAY_TOKEN=your-gateway-token-here

# Database (if applicable)
DATABASE_URL=your-database-url-here

# Other service APIs
# Add your service-specific keys here
EOF

# 5. Create config example files
echo "⚙️ Creating configuration examples..."
if [ -f config.json ]; then
    cp config.json config.example.json
    # Strip out any potential secrets
    sed -i.bak 's/sk-[a-zA-Z0-9-]*/"your-api-key-here"/g' config.example.json
    sed -i.bak 's/"[a-f0-9]\{40,\}"/"your-token-here"/g' config.example.json
    rm config.example.json.bak
    echo "✅ Created config.example.json"
fi

# 6. Test security setup
echo "🧪 Testing security setup..."
pre-commit run --all-files || echo "⚠️ Pre-commit found issues - review and fix"

# 7. Create security checklist
cat > SECURITY_CHECKLIST.md << 'EOF'
# Security Setup Checklist

- [ ] Pre-commit hooks installed and tested
- [ ] .gitignore includes all secret patterns
- [ ] Environment variables documented in .env.example
- [ ] Configuration examples created (without secrets)
- [ ] All developers briefed on security procedures
- [ ] Emergency contact information available
- [ ] Incident response procedures documented

## Before Each Commit
- [ ] Run: `pre-commit run --files <changed-files>`
- [ ] Verify no API keys in changes
- [ ] Check .env files are not staged

## Monthly Security Review
- [ ] Review .gitignore for new patterns
- [ ] Update pre-commit hooks
- [ ] Rotate API keys/tokens
- [ ] Security training for team members
EOF

echo ""
echo "🎉 Repository security setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Review and commit security files: git add . && git commit -m 'Add security safeguards'"
echo "2. Brief all developers on security procedures"
echo "3. Test by running: pre-commit run --all-files"
echo "4. Verify CI/CD includes security checks"
echo ""
echo "⚠️ IMPORTANT: Never commit the following:"
echo "   - .env files (use .env.example instead)"
echo "   - config.json with real secrets (use config.example.json)"
echo "   - Any files with 'sk-', 'auth-', 'secret' in content"