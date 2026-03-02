# Morning War Room Protocol

## What
Daily briefing every morning. Covers full situation, project status, 
and exact daily action items with subagent kickoff commands.

## When
Every morning — 8:30 AM EST, 7 days a week.
Deliver via WhatsApp or Discord.

---

## Structure

### 1. Financial State of the Union (3 min)
- Net worth snapshot (if data changed)
- Cash position vs $30K target
- Debt paydown progress (CC → DCU → Amex loan priority)
- Crypto moves if significant

### 2. Job Search Status (3 min)
- Applications sent yesterday (target: 3/day non-negotiable)
- Any recruiter or interview updates
- Today's 3 target companies
- Warm intro opportunities to pursue

### 3. 3 Nice Things for V (1 min)
- Three specific suggestions for today
- Small, easy, meaningful

### 4. Project Status Check — CODE REVIEW (10 min)
For each active project, I will:
- Check local git status vs GitHub (what's ahead/behind/diverged)
- Read PICKUP.md or README for current state
- Identify the single biggest blocker to first dollar
- Recommend the exact next build task

**Active Projects (priority order):**
1. Cinch-IT / Dead Lead Reactivation — `Cinch-IT/dead-lead-reactivation/`
2. Cinch-IT / AI Prospecting Engine — `Cinch-IT/ai-prospecting-engines/`
3. MetaForge — `Video-Game/`
4. AI Kanban — `work-tools/`

### 5. Today's Subagent Battle Plan (5 min)
Based on project status, I will recommend:
- Which 1-3 subagents to spawn in parallel
- The EXACT prompt to kick each one off
- Which project each agent should work on
- Expected output and success criteria
- Exact terminal commands to run

### 6. Motion Task Updates
- Add today's recommended build tasks to Motion
- Move ready items to "Up Next"
- Mark completed items from yesterday

### 7. Accountability Check (2 min)
- Did you apply to 3 jobs yesterday?
- Any non-essential spending this week?
- Interviews scheduled?
- CC balance at $0?
- DCU extra payment this month?

### 8. Today's #1 Priority
One sentence. The single highest-leverage thing to do today.

---

## Daily Project Code Check Protocol

Every morning before the war room, run this:

```bash
# Check all project status
cd ~/.openclaw/workspace

# Cinch-IT
cd Cinch-IT && git fetch && git status && git log --oneline -3 && cd ..

# Video-Game (MetaForge)
cd Video-Game && git fetch && git status && git log --oneline -3 && cd ..

# work-tools (AI Kanban)
cd work-tools && git fetch && git status && git log --oneline -3 && cd ..
```

Then read PICKUP.md in each project for current dev state.

---

## Revenue Priority Framework

Every build task gets scored before I recommend it:

**Score = (Revenue Impact) x (Speed to Cash) / (Effort)**

- Revenue Impact: Does this directly unlock a paying customer?
- Speed to Cash: How many days until this generates revenue?
- Effort: How many subagent sessions to complete?

**Current Priority Stack (updated daily):**
1. Cinch-IT Dead Lead Reactivation — frontend dashboard (Jay is waiting, 644 leads ready)
2. MetaForge monetization — add paywall before more features
3. Cinch-IT AI Prospecting Engine — scale after DLR is live
4. AI Kanban — internal tool, lowest revenue priority

---

## Subagent Kickoff Template

When recommending a subagent session, I always provide:

```
PROJECT: [name]
GOAL: [what it should accomplish in one session]
PICKUP FILE: [path to PICKUP.md or README]
SUCCESS CRITERIA: [how we know it's done]
SECURITY PREFIX: [always included]
PROMPT: [full copy-paste prompt]
TERMINAL COMMAND: [exact command to run]
```

---

## Standing Rules

- Never recommend building a feature if the current version 
  has no monetization path
- Always check if Jay has responded before prioritizing DLR work
- Job search comes before ALL business building before 10 AM
- If a project has been idle >3 days, flag it and assess whether 
  to kill, pause, or accelerate it
- First dollar beats perfect product every time
