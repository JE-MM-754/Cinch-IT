import {
  CampaignPerformance,
  ContactRecord,
  ForecastRecord,
  InsightRecord,
  LeadRecord,
  MetricCard,
  ModuleId,
  NavItem,
  PipelineDeal,
  SequenceTemplate,
} from "@/lib/types";

export const moduleNavigation: Record<ModuleId, NavItem[]> = {
  reactivation: [
    { label: "Dashboard", href: "/reactivation" },
    { label: "Contacts", href: "/reactivation/contacts" },
    { label: "Sequences", href: "/reactivation/sequences" },
    { label: "Analytics", href: "/reactivation/analytics" },
    { label: "Audit Log", href: "/reactivation/audit-log" },
  ],
  prospecting: [
    { label: "Dashboard", href: "/prospecting" },
    { label: "Discovery", href: "/prospecting/discovery" },
    { label: "Outreach", href: "/prospecting/outreach" },
    { label: "Scoring", href: "/prospecting/scoring" },
  ],
  intelligence: [
    { label: "Dashboard", href: "/intelligence" },
    { label: "Insights", href: "/intelligence/insights" },
    { label: "Pipeline", href: "/intelligence/pipeline" },
    { label: "Forecasting", href: "/intelligence/forecasting" },
  ],
};

export const moduleSummary: Record<ModuleId, { name: string; subtitle: string }> = {
  reactivation: {
    name: "Dead Lead Reactivation",
    subtitle: "Recover pipeline from dormant opportunities with AI outreach",
  },
  prospecting: {
    name: "AI Prospecting Engine",
    subtitle: "Find, qualify, and sequence high-fit accounts across channels",
  },
  intelligence: {
    name: "Sales Intelligence",
    subtitle: "Forecast revenue and prioritize deals with AI guidance",
  },
};

export const reactivationMetrics: MetricCard[] = [
  { label: "Dormant Contacts", value: "1,248", delta: "+7.1%", trend: "up" },
  { label: "Reactivation Rate", value: "29.4%", delta: "+4.3 pts", trend: "up" },
  { label: "Meetings Booked", value: "143", delta: "+18", trend: "up" },
  { label: "Pipeline Recovered", value: "$2.14M", delta: "+$410K", trend: "up" },
];

export const prospectingMetrics: MetricCard[] = [
  { label: "New Accounts Found", value: "2,381", delta: "+12.8%", trend: "up" },
  { label: "Qualified Leads", value: "684", delta: "+9.2%", trend: "up" },
  { label: "Reply Rate", value: "18.6%", delta: "+1.4 pts", trend: "up" },
  { label: "SQL Conversion", value: "32.1%", delta: "-0.8 pts", trend: "down" },
];

export const intelligenceMetrics: MetricCard[] = [
  { label: "Pipeline Coverage", value: "3.7x", delta: "+0.4x", trend: "up" },
  { label: "Commit Accuracy", value: "93%", delta: "+2 pts", trend: "up" },
  { label: "At-Risk Deals", value: "11", delta: "-4", trend: "up" },
  { label: "Q2 Forecast", value: "$6.8M", delta: "+$620K", trend: "up" },
];

export const monthlyPerformance: CampaignPerformance[] = [
  { month: "Sep", reactivated: 42, qualified: 28, pipelineK: 340 },
  { month: "Oct", reactivated: 56, qualified: 33, pipelineK: 420 },
  { month: "Nov", reactivated: 61, qualified: 38, pipelineK: 498 },
  { month: "Dec", reactivated: 65, qualified: 41, pipelineK: 534 },
  { month: "Jan", reactivated: 74, qualified: 46, pipelineK: 588 },
  { month: "Feb", reactivated: 81, qualified: 53, pipelineK: 640 },
];

export const reactivationContacts: ContactRecord[] = [
  { id: "DL-1001", name: "Amelia Shaw", title: "VP Revenue Ops", company: "Northlane Logistics", status: "dormant", lastTouch: "2025-09-04", potentialScore: 91, owner: "J. Patel" },
  { id: "DL-1002", name: "Rafael Ortiz", title: "Head of Sales", company: "Verity Health Systems", status: "in-sequence", lastTouch: "2025-12-19", potentialScore: 88, owner: "D. Kim" },
  { id: "DL-1003", name: "Nina Caldwell", title: "Director of GTM", company: "PioneerStack", status: "re-engaged", lastTouch: "2026-02-14", potentialScore: 85, owner: "A. Singh" },
  { id: "DL-1004", name: "Marcus Lowe", title: "SVP Sales", company: "Asteron Capital", status: "dormant", lastTouch: "2025-08-28", potentialScore: 82, owner: "J. Patel" },
  { id: "DL-1005", name: "Grace Bell", title: "RevOps Lead", company: "Catalyst Security", status: "in-sequence", lastTouch: "2026-01-30", potentialScore: 79, owner: "L. Chen" },
  { id: "DL-1006", name: "Henry Wells", title: "CRO", company: "Summit Data", status: "re-engaged", lastTouch: "2026-02-22", potentialScore: 93, owner: "D. Kim" },
  { id: "DL-1007", name: "Sofia Patel", title: "Sales Director", company: "Brio Manufacturing", status: "dormant", lastTouch: "2025-10-11", potentialScore: 77, owner: "A. Singh" },
  { id: "DL-1008", name: "Ethan Cooper", title: "GTM Operations", company: "SignalForge", status: "in-sequence", lastTouch: "2026-02-08", potentialScore: 86, owner: "L. Chen" },
];

export const sequenceTemplates: SequenceTemplate[] = [
  { id: "SQ-11", name: "Value Reconnect", audience: "Dormant Enterprise", steps: 5, openRate: 51, replyRate: 17, meetings: 24 },
  { id: "SQ-12", name: "Quarterly Trigger", audience: "Budget Cycle Buyers", steps: 4, openRate: 47, replyRate: 15, meetings: 19 },
  { id: "SQ-13", name: "Winback + Case Study", audience: "Competitor Losses", steps: 6, openRate: 56, replyRate: 21, meetings: 32 },
  { id: "SQ-14", name: "Champion Reactivation", audience: "Former Champions", steps: 3, openRate: 63, replyRate: 26, meetings: 18 },
];

export const discoveredLeads: LeadRecord[] = [
  { id: "LD-3001", company: "Monarch Freight", contact: "Claire Morgan", fitScore: 94, intent: "high", channel: "Email", stage: "qualified" },
  { id: "LD-3002", company: "Ivyline Health", contact: "Noah Ramirez", fitScore: 89, intent: "high", channel: "LinkedIn", stage: "working" },
  { id: "LD-3003", company: "PulseGrid", contact: "Evan Brooks", fitScore: 85, intent: "medium", channel: "Phone", stage: "new" },
  { id: "LD-3004", company: "FoundryWorks", contact: "Tara Wells", fitScore: 82, intent: "medium", channel: "Email", stage: "qualified" },
  { id: "LD-3005", company: "Radian Cloud", contact: "Leo Bryant", fitScore: 78, intent: "low", channel: "LinkedIn", stage: "new" },
  { id: "LD-3006", company: "Bluepath AI", contact: "Maya Green", fitScore: 92, intent: "high", channel: "Email", stage: "working" },
];

export const aiInsights: InsightRecord[] = [
  {
    id: "IN-01",
    priority: "High",
    title: "Reactivated leads convert 2.3x faster in healthcare accounts",
    impact: "$480K additional Q2 pipeline",
    recommendation: "Shift 20% of SDR capacity to healthcare dormant leads scoring above 84.",
  },
  {
    id: "IN-02",
    priority: "High",
    title: "Proposal-stage slippage concentrated in west region",
    impact: "11-day average delay",
    recommendation: "Trigger exec sponsor email in week 2 of proposal stage for west region deals.",
  },
  {
    id: "IN-03",
    priority: "Medium",
    title: "Multi-threaded outreach yields 31% higher reply rates",
    impact: "+5.2 pts response lift",
    recommendation: "Add buyer + operator + finance persona touchpoint for enterprise accounts.",
  },
  {
    id: "IN-04",
    priority: "Low",
    title: "Tuesday 10am campaigns underperform Thursday 1pm",
    impact: "-1.8 pts open rate",
    recommendation: "Auto-shift send windows to Thursday 12-2pm for US East segments.",
  },
];

export const pipelineDeals: PipelineDeal[] = [
  { id: "OP-701", account: "Northlane Logistics", stage: "Negotiation", owner: "A. Singh", amountK: 420, closeDate: "2026-03-18", confidence: 74 },
  { id: "OP-702", account: "Verity Health Systems", stage: "Proposal", owner: "J. Patel", amountK: 360, closeDate: "2026-03-30", confidence: 68 },
  { id: "OP-703", account: "Summit Data", stage: "Closed Won", owner: "D. Kim", amountK: 290, closeDate: "2026-02-22", confidence: 100 },
  { id: "OP-704", account: "SignalForge", stage: "Discovery", owner: "L. Chen", amountK: 180, closeDate: "2026-04-12", confidence: 47 },
  { id: "OP-705", account: "Catalyst Security", stage: "Negotiation", owner: "A. Singh", amountK: 510, closeDate: "2026-03-27", confidence: 79 },
  { id: "OP-706", account: "Brio Manufacturing", stage: "Proposal", owner: "J. Patel", amountK: 250, closeDate: "2026-04-08", confidence: 63 },
];

export const forecastSeries: ForecastRecord[] = [
  { month: "Mar", commit: 1.42, bestCase: 1.78, aiProjection: 1.69 },
  { month: "Apr", commit: 1.55, bestCase: 1.94, aiProjection: 1.88 },
  { month: "May", commit: 1.61, bestCase: 2.02, aiProjection: 1.96 },
  { month: "Jun", commit: 1.71, bestCase: 2.14, aiProjection: 2.08 },
  { month: "Jul", commit: 1.79, bestCase: 2.27, aiProjection: 2.21 },
  { month: "Aug", commit: 1.86, bestCase: 2.33, aiProjection: 2.29 },
];

export const auditLog = [
  { time: "2026-02-28 09:14", action: "AI identified 42 at-risk dormant contacts", actor: "Reactivation Bot", result: "Queued" },
  { time: "2026-02-28 10:02", action: "Generated personalized email copy", actor: "AI Composer", result: "288 messages drafted" },
  { time: "2026-02-28 10:47", action: "Lead enrichment via firmographic model", actor: "Prospecting Bot", result: "117 accounts scored" },
  { time: "2026-02-28 11:18", action: "Forecast updated from fresh activity signals", actor: "Intelligence Engine", result: "+$210K AI projection" },
  { time: "2026-02-28 11:59", action: "Escalated proposal-stage deal risk", actor: "Deal Risk Monitor", result: "Owner notified" },
];
