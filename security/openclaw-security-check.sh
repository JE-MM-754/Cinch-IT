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
