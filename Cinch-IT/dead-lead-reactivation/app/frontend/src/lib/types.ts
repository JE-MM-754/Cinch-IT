export type ModuleId = "reactivation" | "prospecting" | "intelligence";

export interface NavItem {
  label: string;
  href: string;
}

export interface MetricCard {
  label: string;
  value: string;
  delta: string;
  trend: "up" | "down" | "flat";
}

export interface ContactRecord {
  id: string;
  name: string;
  title: string;
  company: string;
  status: "dormant" | "re-engaged" | "in-sequence";
  lastTouch: string;
  potentialScore: number;
  owner: string;
}

export interface SequenceTemplate {
  id: string;
  name: string;
  audience: string;
  steps: number;
  openRate: number;
  replyRate: number;
  meetings: number;
}

export interface LeadRecord {
  id: string;
  company: string;
  contact: string;
  fitScore: number;
  intent: "high" | "medium" | "low";
  channel: "Email" | "LinkedIn" | "Phone";
  stage: "new" | "qualified" | "working";
}

export interface CampaignPerformance {
  month: string;
  reactivated: number;
  qualified: number;
  pipelineK: number;
}

export interface ForecastRecord {
  month: string;
  commit: number;
  bestCase: number;
  aiProjection: number;
}

export interface InsightRecord {
  id: string;
  priority: "High" | "Medium" | "Low";
  title: string;
  impact: string;
  recommendation: string;
}

export interface PipelineDeal {
  id: string;
  account: string;
  stage: "Discovery" | "Proposal" | "Negotiation" | "Closed Won";
  owner: string;
  amountK: number;
  closeDate: string;
  confidence: number;
}
