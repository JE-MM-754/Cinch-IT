#!/bin/bash
# Pre-commit hook installer for API key protection
# Run this in every repository where Codex/Claude will work

echo "🛡️ Installing pre-commit security hooks..."

# Install pre-commit if not exists
if ! command -v pre-commit &> /dev/null; then
    echo "Installing pre-commit..."
    pip install pre-commit
fi

# Create .pre-commit-config.yaml
cat > .pre-commit-config.yaml << 'EOF'
repos:
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
        args: ['--baseline', '.secrets.baseline']
  
  - repo: https://github.com/gitguardian/ggshield
    rev: v1.25.0
    hooks:
      - id: ggshield
        language: python
        stages: [commit]
  
  - repo: local
    hooks:
      - id: openclaw-security-check
        name: OpenClaw Security Check
        entry: ./security/openclaw-security-check.sh
        language: script
        files: '.*\.(json|md|js|ts|py|env)$'
EOF

# Create OpenClaw-specific security check script
mkdir -p security
cat > security/openclaw-security-check.sh << 'EOF'
#!/bin/bash
# OpenClaw-specific security scanner

echo "🔍 Running OpenClaw security scan..."

# Check for specific patterns
DANGEROUS_PATTERNS=(
    "sk-ant-" # pragma: allowlist secret
    "sk-proj-"
    "gpt-"
    "claude-"
    "anthropic.*key"
    "openai.*key"
    "gateway.*token"
    "466f1578ae7898fa19e4cdb834544ab75cf6e4ad169d799e"
)

for pattern in "${DANGEROUS_PATTERNS[@]}"; do
    if git diff --cached --name-only | xargs grep -l "$pattern" 2>/dev/null; then
        echo "❌ SECURITY VIOLATION: Pattern '$pattern' found in staged files"
        echo "🚨 COMMIT BLOCKED - Remove secrets before committing"
        exit 1
    fi
done

# Check for common secret file names
DANGEROUS_FILES=(
    "*auth-profiles*"
    "*backup*.json"
    "*SYSTEM_BACKUP*"
    "*secret*"
    "*credential*"
    ".env"
)

for file_pattern in "${DANGEROUS_FILES[@]}"; do
    if git diff --cached --name-only | grep -E "$file_pattern" 2>/dev/null; then
        echo "❌ SECURITY VIOLATION: Dangerous file pattern '$file_pattern' in commit"
        echo "🚨 COMMIT BLOCKED - Never commit credential files"
        exit 1
    fi
done

echo "✅ OpenClaw security check passed"
EOF

chmod +x security/openclaw-security-check.sh

# Install hooks
pre-commit install

echo "✅ Pre-commit security hooks installed successfully"
echo "💡 Test with: pre-commit run --all-files"