# Fortescue Calls — Raw Notes
*Captured 2026-03-02*

---

## Call 1: Fortescue Intro / Discovery

### Customer Context
- **Mark** (customer) — looking at HPC environment projects
- **Gaurav** (customer) — most interested in MCP Gateway + AI Gateway
- **Environment:** 72 nodes of H200 GPUs (possibly some S200 — unclear from audio)
- **Current clouds:** AWS (having issues) + GCP (also having issues) — moved to GCP for cost, still availability issues
- **On-prem ambition:** Want flexibility to run workloads off-cloud on physical servers to support decarbonizing efforts
- **Base:** Australia, but compute currently running in US/Europe (Australia regions hard)
- **SaaS constraint:** SaaS only viable if hosted in Australia. Currently in Europe = blocker.
- **Team size:** Light team. Wants partner to handle as much management as possible.
- **Kubernetes:** Yes, in some areas. Also using **SWERM** clusters — need a Kubernetes-to-SWERM bridge (Slinky)
- **Auth stack:** Legacy apps with no sophisticated auth. OAuth workflow issues for ~6 weeks. Want to offload OAuth paths to MCP gateway via token exchange.
- **Competitor dynamic:** Databricks recently approved internally — TrueFoundry must articulate delta value vs. Databricks
- **Azure:** Currently using Azure MCP + container registry. Azure observability is good.
- **Decision timeline:** "Tomorrow if we find the right product" — highly motivated buyer

### Pain Points
1. **No vendor lock-in** — primary. Data scientists need to focus on experiments, not compute environments.
2. **GPU availability + cost** — on AWS and GCP both failing them
3. **OAuth/auth complexity** — 6 weeks of pain, want centralized token exchange
4. **AI/LLM governance** — starting on OpenAI, seeing pressure for Gemini + Claude, need centralized egress + key management
5. **Observability** — want centralized cost management, not checking each provider separately
6. **Job failures** — don't want failed jobs discovered next day; real-time monitoring needed
7. **Multi-cloud flexibility** — GCP, AWS, Azure + physical servers in future

### Technical Stack
- PyTorch, Weights & Biases (experiment tracking)
- Transformer-based deep learning models
- Inference: real-time, deployed in cloud, integrated into on-site applications for decision-making
- Inference hardware: AWS, GPU type unknown to them
- Kubernetes + SWERM hybrid
- Azure JWT tokens — want external identity passthrough
- OpenAI primary, exploring Gemini + Claude

### What TrueFoundry Showed / Key Questions Asked
- Nikunj asked: training vs inference jobs? Batch vs real-time? CPUs vs GPUs? Kubernetes?
- Fortescue asked: Australian customers? → Yes (CVS case study)
- CVS use case: TrueFoundry deployment + AI gateway module, ~500M requests at scale, manages GPUs on GCP
- NVIDIA case study: GPU cluster utilization agent, fine-tuning LLMs
- **Pricing discussed:**
  - 12-20 developers
  - 5,500 active OpenAI users, millions of daily comms
  - Starting price: ~$150K with SLA → up to $350K depending on request scale
  - No GPU cap on developer-based pricing

### Jamie's Observations — Call 1
- ✅ Great discovery questions asked
- ❌ Didn't get to a TrueFoundry overview until they were out of time — had to ask for 10 extra min
- ❌ **Deck starts wrong** — slide 2 is team/backers/trust. Nobody cares yet. Should start with "what's in it for them"
- 💡 **Idea:** "Drag through the glass" slide — show TrueFoundry deeply understands customer pain BEFORE the who-is-TrueFoundry credibility slide. Customer is the hero.
- ❌ Didn't probe enough on future use cases to plant seeds for expansion vision
- ❌ Opportunity missed to nail next steps — customer is super interested, call ended without clear close on POC/next steps
- ❌ Pricing discussion was too complex — hard to confirm budget alignment. Simpler pricing scalar needed.
- 💡 Pricing feels low. Opportunity to test higher pricing given scale of this customer.

---

## Call 2: AI Gateway Capability Demo

### Key Technical Q&A
- **External calls from AI Gateway?** — Jamie's note: need to find answer
- **Sydney/Canberra regions?** → Yes
- **Virtual account in hybrid env?** → Yes
- **Developer assignment + cost tracking?** → Each dev gets personal access token. Each app gets app token. Dev token expires on offboarding.
- **Entra SSO integration?** → Yes, SSO via Entra, teams auto-created
- **JWT tokens?** → Yes, access tokens are JWT
- **Azure JWT tokens directly?** → Yes, via external identities
- **CI/CD pipeline config?** → Yes
- **Terraform modules?** → No, recommend Kubernetes instead
- **Centralized model observatory + threshold monitoring?** → Yes, but no drift monitoring. Not an evaluation platform — they're an AI gateway.
- **MCP Gateway:** Handles OAuth offloading, token exchange — key differentiator for Fortescue auth pain

### Product Clarifications (Jamie Learning)
- **AI Gateway:** Lightweight routing layer connecting apps to LLMs, Tools, Agents — provides governance, monitoring, control
- **AI Deployments:** Orchestrate Kubernetes to deploy scalable, cost-optimized GenAI components in your own cloud/on-prem VPC
- **Model Gateway:** Add credentials for providers (OpenAI, Anthropic, Databricks, Google, etc.)
- **Virtual models:** Combination of multiple models — need to assess if this is a differentiator or commodity
- **Priority-based routing:** Need to understand if this differentiates vs competitors
- **No TrueFoundry SDK lock-in:** Prevents vendor lock-in — big value prop, NOT being emphasized enough
- **Control plane vs compute plane:** Customer was confused too. Need simple language here.
  - **Compute plane** = where the GPU/compute jobs actually run
  - **Control plane** = where logs, monitoring, orchestration live

### Jamie's Observations — Call 2
- ❌ **Started Call 2 again with team/backing/Fortune 500 trust slides.** This is call 2. They know who you are. Lead with value.
- ❌ Led with "general engineering support" — expensive thing to lead with, hurts 10x growth from delivery perspective. Could be a premium tier instead.
- ❌ Same "drag through the glass" opportunity missed — jumped straight into features without executive storytelling
- ❌ After product overview, no "what resonates?" question. Left insight on the table.
- ❌ Demo is very feature/function. Needed: "here's what's different and why it matters vs. competitors"
- 💡 **Battle deck idea:** Create competitive battle card vs MCP gateway competitors to help guide buyer evaluation. Customer said they're already looking at alternatives.
- 💡 **Interactive click demo idea:** Shareable click-through demo for customer engineers. Helps with infosec reviews, pre-sales enablement, creates champions.
- ✅ **Akshay strong close Q:** "What's the pathway to a POC? Who else do we need to show this to?" — good deal advancement
- ✅ **Akshay strong competitive Q:** "What have you seen vs other competitors so far?" — smart positioning question
- ✅ **Abhishek great discovery Q:** "Initial thoughts after the demo — anything you really liked, anything missing?"
- ✅ Good ending from Akshay — relationship/team angle on fast-moving space
- ❌ Lost deal control without helping guide "Why TrueFoundry" evaluation framework
- ❌ No clear battle narrative vs. Azure/Databricks specifically (Fortescue already approved Databricks internally)

---

## Key Gaps Jamie Needs to Fill
- [ ] How to talk about AI Gateway in depth (now better — see above)
- [ ] How to talk about AI Deployments
- [ ] Control plane vs compute plane simple language
- [ ] Vendor lock-in prevention angle (no TrueFoundry SDK) — major talking point
- [ ] Competitive positioning: TrueFoundry vs Databricks specifically (this deal's key question)
- [ ] TrueFoundry vs Azure MCP (Fortescue's current stack)
- [ ] Australian customer list / regional availability
- [ ] POC motion — what does a successful POC look like, who drives it?
- [ ] Pricing simplification — what's the simple scalar story?

---

## Strategic Observations for Jamie's Interview
- **Sales process gap:** This is a founder-led, very technical pitch. Not systematized for scalable sales reps.
- **First-call structure needs work:** Value-first, credibility-second. Customer is the hero, TrueFoundry is the guide.
- **Battle deck needed:** Competitive evaluation framework to guide buyers through "Why TrueFoundry"
- **POC process needs tightening:** End every demo with clear POC next steps and success criteria
- **Pricing needs simplification:** Complex pricing scalar caused confusion. Simpler = faster deal velocity.
- **This is YOUR pitch for VP Sales role:** You saw the gaps. You know exactly what to build. Reference these observations when they ask "what would you do in the first 30/60/90 days."
