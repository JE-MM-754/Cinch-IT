# AI AGENT SECURITY GUIDE
*Preventing credential leaks when working with Codex, Claude Code, and other AI coding agents*

## 🎯 CORE PRINCIPLE
**AI agents are powerful but not security-aware by default. YOU must build the guardrails.**

## 🛡️ MULTI-LAYER DEFENSE STRATEGY

### **Layer 1: Prevention (Stop secrets from entering)**
1. **Use environment variables** for all secrets
2. **Never put real credentials** in config files  
3. **Create .example files** with dummy values
4. **Educate agents** about security requirements in prompts

### **Layer 2: Detection (Catch secrets before commit)**
1. **Pre-commit hooks** that scan for secret patterns
2. **Enhanced .gitignore** with comprehensive secret patterns
3. **Manual verification** before any git operations
4. **CI/CD security scanning** as backup

### **Layer 3: Response (Fast remediation when prevention fails)**
1. **Immediate credential revocation** procedures
2. **Git history cleaning** tools and processes
3. **Incident response** templates and checklists
4. **Post-incident** learning and improvement

## 🤖 WORKING SAFELY WITH AI AGENTS

### **Before Starting Any AI Coding Session:**

1. **Run repository security setup:**
   ```bash
   bash ~/.openclaw/workspace/security/secure-repo-setup.sh
   ```

2. **Always include security prefix in prompts** (see template)

3. **Verify security tools are working:**
   ```bash
   pre-commit run --all-files
   ```

### **Essential Prompt Security Patterns:**

```
🚨 MANDATORY SECURITY PREFIX FOR ALL AI AGENT PROMPTS:

CRITICAL SECURITY REQUIREMENTS:
1. NEVER commit files containing API keys (sk-ant-, sk-proj-, etc.)
2. BEFORE any git commit, run: git diff --cached | grep -E "(sk-|auth|secret)"
3. If secrets found, STOP and ask for guidance
4. Use .env.example with dummy values, never real secrets
5. ACKNOWLEDGE these requirements before proceeding

[Your actual prompt here]
```

### **High-Risk Scenarios (Extra Vigilance Required):**

1. **Configuration file work** - Most likely to contain secrets
2. **Backup/restore operations** - Often copy sensitive files
3. **Environment setup** - May hardcode credentials temporarily
4. **Testing/debugging** - May create temp files with secrets
5. **Documentation** - May accidentally include real examples

### **Red Flag Patterns to Watch For:**

**In AI Agent Responses:**
- Suggests hardcoding API keys
- Creates config files without environment variable patterns
- Commits files without running security checks first
- Ignores or bypasses security requirements

**In Code Changes:**
- Files with "auth", "secret", "credential", "backup" in names
- Config files with real API key patterns
- .env files being committed (should only be .env.example)
- Any string starting with "sk-", "gpt-", "claude-"

## ⚙️ REPOSITORY SECURITY SETUP

### **For Every New Repository:**

1. **Copy security template:**
   ```bash
   cp ~/.openclaw/workspace/security/secure-gitignore-template .gitignore
   ```

2. **Install pre-commit hooks:**
   ```bash
   bash ~/.openclaw/workspace/security/pre-commit-hook-setup.sh
   ```

3. **Create configuration templates:**
   ```bash
   # If you have config.json with secrets:
   cp config.json config.example.json
   # Replace real secrets with placeholders
   sed -i 's/sk-[a-zA-Z0-9-]*/"YOUR_API_KEY_HERE"/g' config.example.json
   ```

4. **Test security setup:**
   ```bash
   pre-commit run --all-files
   ```

### **Security Checklist for AI Agents:**

Before delegating work to any AI coding agent:

- [ ] Repository has enhanced .gitignore
- [ ] Pre-commit hooks installed and tested  
- [ ] All prompts include security requirements
- [ ] Agent acknowledges security requirements
- [ ] .env.example created (no real secrets)
- [ ] Emergency response procedures documented

## 🚨 IF SECRETS GET COMMITTED ANYWAY

### **Immediate Actions (< 10 minutes):**

1. **Revoke exposed credentials immediately:**
   - Anthropic: https://console.anthropic.com/account/keys
   - OpenAI: https://platform.openai.com/api-keys
   - OpenClaw: `openclaw configure --reset-gateway-token`

2. **Stop the bleeding:**
   ```bash
   # Remove from working directory
   git reset HEAD <secret-file>
   git checkout -- <secret-file>
   ```

3. **Alert team if public repository**

### **Git History Cleanup:**

```bash
# For single file:
git filter-branch --index-filter 'git rm --cached --ignore-unmatch <secret-file>' HEAD

# For content patterns:
bfg --replace-text passwords.txt  # Create file with secrets to redact

# Force push cleaned history:
git push --force-with-lease origin main
```

### **Follow full incident response** template in security/incident-response-template.md

## 📚 ADVANCED SECURITY MEASURES

### **For High-Security Environments:**

1. **Separate AI agent accounts** with limited permissions
2. **Code review requirements** before merging AI-generated code
3. **Sandboxed environments** for AI agent work
4. **Regular security audits** of AI-generated code
5. **Automated secret scanning** in CI/CD pipeline

### **Monitoring and Alerting:**

1. **GitHub secret scanning** enabled on all repos
2. **API usage monitoring** for unusual patterns
3. **Failed pre-commit hook alerts**
4. **Regular access reviews** for AI agent accounts

## 🎯 SUCCESS METRICS

**You know your security is working when:**
- Pre-commit hooks catch 100% of attempted secret commits
- AI agents consistently follow security prompts
- Zero incidents of secrets in production repositories  
- Team members instinctively verify security before commits
- Incident response can be executed in < 1 hour when needed

## 📞 EMERGENCY CONTACTS

**Security Incident Response Team:**
- Primary: [Your contact]
- Secondary: [Backup contact]
- Emergency escalation: [Manager/Security team]

**Service Provider Support:**
- Anthropic Support: support@anthropic.com
- OpenAI Support: help.openai.com
- GitHub Security: https://github.com/security

---

*Remember: AI agents are tools. The responsibility for security lies with the human operator.*