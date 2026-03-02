#!/bin/bash
# Test script to verify security setup is working properly

echo "🧪 Testing OpenClaw Security Setup..."
echo ""

PASSED=0
FAILED=0

# Test 1: Check if .gitignore has security patterns
echo "📝 Test 1: Checking .gitignore security patterns..."
if grep -q "sk-ant-" .gitignore && grep -q "auth-profiles" .gitignore; then
    echo "✅ .gitignore has security patterns"
    ((PASSED++))
else
    echo "❌ .gitignore missing security patterns"
    ((FAILED++))
fi
echo ""

# Test 2: Check if pre-commit is installed
echo "🔧 Test 2: Checking pre-commit installation..."
if command -v pre-commit &> /dev/null && [ -f .pre-commit-config.yaml ]; then
    echo "✅ Pre-commit hooks configured"
    ((PASSED++))
else
    echo "❌ Pre-commit hooks not configured"
    ((FAILED++))
fi
echo ""

# Test 3: Test secret detection with dummy secret
echo "🔍 Test 3: Testing secret detection..."
# Create a temporary file with a fake secret
echo "sk-ant-test-secret-12345" > temp_secret_test.txt
git add temp_secret_test.txt 2>/dev/null

# Try to run pre-commit
if pre-commit run --files temp_secret_test.txt 2>&1 | grep -q "BLOCKED\|blocked\|SECRET\|secret"; then
    echo "✅ Secret detection working"
    ((PASSED++))
else
    echo "❌ Secret detection not working"
    ((FAILED++))
fi

# Cleanup
git reset HEAD temp_secret_test.txt 2>/dev/null
rm -f temp_secret_test.txt
echo ""

# Test 4: Check for security documentation
echo "📚 Test 4: Checking security documentation..."
if [ -f security/ai-agent-security-guide.md ] && [ -f security/secure-agent-prompt-template.md ]; then
    echo "✅ Security documentation present"
    ((PASSED++))
else
    echo "❌ Security documentation missing"
    ((FAILED++))
fi
echo ""

# Test 5: Check environment template
echo "⚙️ Test 5: Checking environment template..."
if [ -f .env.example ] && ! [ -f .env ]; then
    echo "✅ Environment template configured correctly"
    ((PASSED++))
else
    echo "❌ Environment configuration needs attention"
    ((FAILED++))
fi
echo ""

# Summary
echo "📊 Security Setup Test Results:"
echo "✅ Passed: $PASSED"
echo "❌ Failed: $FAILED"
echo ""

if [ $FAILED -eq 0 ]; then
    echo "🎉 All security tests passed! Repository is secure for AI agent work."
    echo ""
    echo "🚀 Next steps:"
    echo "1. Commit security setup: git add . && git commit -m 'Add comprehensive security safeguards'"
    echo "2. Brief team on security procedures"
    echo "3. Always use security prefix in AI agent prompts"
else
    echo "⚠️ Some security tests failed. Please review and fix issues before using AI agents."
    echo ""
    echo "🔧 Quick fixes:"
    echo "1. Run: bash security/secure-repo-setup.sh"
    echo "2. Install pre-commit: pip install pre-commit && pre-commit install"  
    echo "3. Review .gitignore and add missing patterns"
fi