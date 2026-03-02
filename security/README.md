# 🛡️ OPENCLAW SECURITY SYSTEM
*Bulletproof protection against API key leaks when using AI coding agents*

## 🚨 THE PROBLEM WE SOLVED
**March 1, 2026**: API keys were accidentally committed to public GitHub repository by AI agent, exposing:
- Anthropic API key (`sk-ant-api03-...`)
- OpenAI API key (`sk-proj-...`)  
- OpenClaw gateway token

**This system ensures it NEVER happens again.**

## 🎯 COMPREHENSIVE DEFENSE STRATEGY

### **Multi-Layer Security:**
1. **Prevention** - Stop secrets from entering code
2. **Detection** - Catch secrets before they get committed  
3. **Response** - Fast remediation when prevention fails

### **AI Agent Protection:**
- Secure prompting templates with mandatory security requirements
- Pre-commit hooks that block dangerous commits
- Enhanced .gitignore patterns for all secret types
- Incident response procedures for fast recovery

## 🚀 QUICK START

### **For New Repositories:**
```bash
# 1. Set up comprehensive security
bash ~/.openclaw/workspace/security/secure-repo-setup.sh

# 2. Test everything works
bash ~/.openclaw/workspace/security/test-security-setup.sh

# 3. Commit security setup
git add . && git commit -m "Add comprehensive security safeguards"
```

### **For Existing Repositories:**
```bash
# 1. Add enhanced .gitignore
cat ~/.openclaw/workspace/security/secure-gitignore-template >> .gitignore

# 2. Install pre-commit hooks
bash ~/.openclaw/workspace/security/pre-commit-hook-setup.sh

# 3. Test security setup
bash ~/.openclaw/workspace/security/test-security-setup.sh
```

## 🤖 WORKING WITH AI AGENTS (CRITICAL)

### **ALWAYS Use This Prompt Prefix:**
```
🚨 CRITICAL SECURITY REQUIREMENTS - READ FIRST:

1. NEVER commit files containing API keys (sk-ant-, sk-proj-, etc.)
2. BEFORE any git commit, run: git diff --cached | grep -E "(sk-|auth|secret)"
3. If ANY secrets found, STOP and ask for guidance
4. Use .env.example with dummy values, never real secrets
5. ACKNOWLEDGE these requirements before proceeding

[Your actual prompt here]
```

### **High-Risk AI Agent Tasks:**
- Configuration file modifications
- Backup/restore operations  
- Environment setup scripts
- Testing/debugging code
- Documentation with examples

**Extra vigilance required for these scenarios.**

## 📁 SECURITY TOOLKIT

| File | Purpose |
|------|---------|
| `secure-repo-setup.sh` | Complete repository security setup |
| `pre-commit-hook-setup.sh` | Install secret-detection hooks |
| `secure-gitignore-template` | Enhanced .gitignore patterns |
| `secure-agent-prompt-template.md` | Safe AI agent prompting |
| `incident-response-template.md` | Emergency response procedures |
| `ai-agent-security-guide.md` | Comprehensive security guide |
| `test-security-setup.sh` | Verify security is working |

## 🔧 TECHNICAL DETAILS

### **Pre-Commit Hook Protection:**
- **GitGuardian** - Professional secret scanning
- **detect-secrets** - Baseline secret detection
- **Custom OpenClaw patterns** - Specific to our API keys/tokens

### **Enhanced .gitignore Patterns:**
```
# API Keys & Secrets  
**/sk-*
**/*secret*
**/*credential*
auth-profiles*.json
*-backup-*.json
SYSTEM_BACKUP_*.md

# OpenClaw Specific
.openclaw/
openclaw.config.json
gateway-token*
```

### **Security Testing:**
```bash
# Test pre-commit hooks
pre-commit run --all-files

# Test specific file
pre-commit run --files suspicious-file.json

# Verify .gitignore patterns
git check-ignore secret-file.json
```

## 🚨 EMERGENCY PROCEDURES

### **If Secrets Get Committed:**

**1. IMMEDIATE (< 10 minutes):**
```bash
# Revoke credentials
# - Anthropic: https://console.anthropic.com/account/keys
# - OpenAI: https://platform.openai.com/api-keys
# - OpenClaw: openclaw configure --reset-gateway-token
```

**2. CLEAN GIT HISTORY:**
```bash
# Remove secret files
git filter-branch --index-filter 'git rm --cached --ignore-unmatch secret-file.json' HEAD

# Force push cleaned history
git push --force-with-lease origin main
```

**3. FOLLOW INCIDENT RESPONSE:**
- Use `incident-response-template.md` 
- Document everything for learning
- Update security procedures

## 📊 SUCCESS METRICS

**Your security is working when:**
- ✅ Pre-commit hooks catch 100% of secret commits
- ✅ AI agents consistently follow security prompts  
- ✅ Zero secrets in production repositories
- ✅ Team instinctively verifies security before commits
- ✅ Incident response executes in < 1 hour

## 🎓 TEAM TRAINING

### **Required Reading for All Developers:**
1. `ai-agent-security-guide.md` - Complete security guide
2. `secure-agent-prompt-template.md` - Safe prompting patterns
3. `incident-response-template.md` - Emergency procedures

### **Monthly Security Checklist:**
- [ ] Review .gitignore for new patterns
- [ ] Update pre-commit hooks
- [ ] Rotate API keys/tokens  
- [ ] Security refresher training
- [ ] Test incident response procedures

## 📞 EMERGENCY CONTACTS

**Security Incident Response:**
- Primary: Jamie Erickson
- GitHub Security: https://github.com/security
- Anthropic Support: support@anthropic.com
- OpenAI Support: help.openai.com

## 🔍 VERIFICATION

**Test your setup:**
```bash
bash security/test-security-setup.sh
```

**Expected output:**
```
✅ Passed: 5
❌ Failed: 0
🎉 All security tests passed! Repository is secure for AI agent work.
```

---

## 💡 LESSONS LEARNED

**From March 1, 2026 Incident:**
1. AI agents need explicit security guidance in prompts
2. Pre-commit hooks are essential, not optional
3. .gitignore must be comprehensive from day one
4. Fast incident response minimizes damage
5. Multiple security layers prevent single points of failure

**This system is the result of learning from that incident. Use it.**

---

*Last updated: March 1, 2026*  
*Next review: Monthly or after any security incident*