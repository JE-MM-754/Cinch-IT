# Multi-Agent CinchIT Development Example

## Current State
- **Claude CLI:** Building main CinchIT AI Prospecting Engine (session: amber-tidepool)
- **Codex GUI:** Available for interactive tasks
- **Pi CLI:** Available for quick utilities

## Multi-Agent Task Distribution

### **Claude CLI (Background Build)**
**Current Task:** Full CinchIT MVP
- FastAPI backend with PostgreSQL
- AI scoring engine with Claude Haiku
- Signal detection pipeline  
- Next.js dashboard frontend
- **Status:** In progress, running autonomously

### **Codex GUI (Interactive Development)**
**Suggested Tasks while Claude works:**
1. **Signal Detection Algorithms:** Prototype the job posting analysis logic interactively
2. **API Design:** Design and test the prospect scoring API endpoints
3. **Data Schema:** Design the PostgreSQL schema for prospect data
4. **AI Prompt Engineering:** Develop the Claude Haiku scoring prompts

### **Pi CLI (Quick Utilities)**
**Parallel Tasks:**
1. **Data Processing Scripts:** Parse existing contact CSV files
2. **Testing Utilities:** Create prospect data generators for testing  
3. **Integration Scripts:** Build connectors for Apollo.io API
4. **Monitoring Tools:** Create health check scripts for the pipeline

## Coordination Strategy

### File-Based Handoffs
```
shared/
├── schemas/           # Codex designs → Claude implements
├── algorithms/        # Codex prototypes → Pi productionizes  
├── prompts/          # Codex develops → Claude integrates
└── test-data/        # Pi generates → all agents use
```

### Git Branch Strategy
```
main                  # Production ready code
├── claude/mvp        # Claude's full build branch
├── codex/prototypes  # Interactive development branch  
└── pi/utilities      # Quick scripts and tools branch
```

### Communication Protocol
1. **Codex designs** → saves to `shared/schemas/`
2. **Claude implements** → reads from `shared/schemas/`
3. **Pi builds utilities** → supports both other agents
4. **Daily integration** → merge working features to main

## Example Workflow (Right Now)

### **Immediate Parallel Tasks:**

**1. Codex GUI (Interactive):**
Open Codex and work on:
```python
# Design the prospect scoring algorithm
def score_prospect_urgency(signals, company_profile, icp_match):
    """
    Interactive development of the core scoring logic
    Test different weightings, see immediate results
    """
    pass
```

**2. Pi CLI (Background Utility):**
```bash
# While Codex works interactively, Pi builds data processor
cd ~/Desktop/Business\ Ventures/Cinch\ IT/
exec pty:true background:true command:"pi 'Create a Python script that parses Contact Search Results - CinchIT.csv and extracts: company name, industry, employee count, and contact info. Output as JSON for the AI scoring engine.'"
```

**3. Claude CLI (Continuing):**
Let Claude continue the main MVP build without interruption

### **Monitoring All Agents:**
```bash
# See all active coding work
process action:list

# Check Claude's main build progress
process action:log sessionId:amber-tidepool limit:5

# Check Pi's utility progress  
process action:log sessionId:[new-pi-session] limit:5

# Codex progress: Manual monitoring in GUI
```

## Benefits of This Approach

1. **Parallel Development:** 3x faster than sequential
2. **Specialized Tools:** Each agent optimized for different tasks
3. **Interactive + Automated:** Best of both worlds
4. **Risk Mitigation:** If one agent fails, others continue
5. **Skill Matching:** Right tool for each job type

## Next Steps

1. **Start Pi utility now** (while Claude works)
2. **Open Codex for algorithm design** (interactive)
3. **Coordinate via shared files** (schemas, prompts, data)
4. **Daily integration** (merge working pieces)