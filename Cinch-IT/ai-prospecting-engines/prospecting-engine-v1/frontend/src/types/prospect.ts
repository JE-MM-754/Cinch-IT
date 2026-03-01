// TypeScript definitions for Cinch IT AI Prospecting Engine
// Updated by MoneyMachine when AI engine APIs change

export interface Company {
  id: number;
  name: string;
  website: string;
  industry: string;
  employee_count: number;
  location: string;
  founded_year: number | null;
  revenue_estimate: string;
  technology_stack: string[];
  pain_points: string[];
  growth_signals: string[];
  news_events: string[];
  funding_status: string;
  created_at: string;
  updated_at: string;
}

export interface Contact {
  id: number;
  company_id: number;
  first_name: string;
  last_name: string;
  title: string;
  email: string;
  linkedin_url: string;
  phone: string | null;
  decision_maker_score: number; // 0-100
  contact_quality: 'high' | 'medium' | 'low';
  apollo_enriched: boolean;
  verification_status: 'verified' | 'unverified' | 'bounced';
  created_at: string;
  updated_at: string;
}

export interface LeadScore {
  company_id: number;
  overall_score: number; // 0-100
  size_score: number;
  industry_score: number;
  technology_score: number;
  growth_score: number;
  location_score: number;
  ai_confidence: number; // 0-1
  human_override: boolean;
  qualification_status: 'hot' | 'warm' | 'cold' | 'disqualified';
  last_updated: string;
  score_breakdown: {
    criteria: string;
    score: number;
    weight: number;
    reason: string;
  }[];
}

export interface Prospect {
  company: Company;
  primary_contact: Contact;
  lead_score: LeadScore;
  outreach_history: OutreachActivity[];
  last_activity: string | null;
  assigned_to: string | null;
  notes: string;
  tags: string[];
}

export interface OutreachActivity {
  id: number;
  contact_id: number;
  campaign_id: number;
  channel: 'email' | 'linkedin' | 'phone';
  message_type: 'connection_request' | 'cold_email' | 'follow_up' | 'meeting_request';
  subject: string;
  content: string;
  sent_at: string;
  status: 'queued' | 'sent' | 'delivered' | 'opened' | 'clicked' | 'replied' | 'bounced' | 'failed';
  response_received: boolean;
  response_content: string | null;
  response_sentiment: 'positive' | 'neutral' | 'negative' | null;
  meeting_booked: boolean;
  is_test: boolean;
}

export interface Campaign {
  id: number;
  name: string;
  description: string;
  channel: 'email' | 'linkedin' | 'multi_touch';
  target_criteria: {
    min_score: number;
    industries: string[];
    employee_range: [number, number];
    locations: string[];
  };
  sequence_steps: SequenceStep[];
  status: 'draft' | 'active' | 'paused' | 'completed';
  created_at: string;
  performance_metrics: CampaignMetrics;
}

export interface SequenceStep {
  step_number: number;
  delay_days: number;
  channel: 'email' | 'linkedin';
  message_type: string;
  subject_template: string;
  content_template: string;
  personalization_variables: string[];
  is_active: boolean;
}

export interface CampaignMetrics {
  total_sent: number;
  total_delivered: number;
  total_opened: number;
  total_clicked: number;
  total_replied: number;
  meetings_booked: number;
  response_rate: number;
  meeting_rate: number;
  cost_per_lead: number;
}

export interface ProspectingDashboard {
  summary: {
    total_prospects: number;
    qualified_leads: number;
    active_campaigns: number;
    meetings_this_month: number;
    pipeline_value: number;
  };
  lead_funnel: {
    discovered: number;
    qualified: number;
    contacted: number;
    responded: number;
    meetings: number;
    opportunities: number;
  };
  performance: {
    prospect_discovery_rate: number; // per week
    qualification_accuracy: number; // %
    outreach_response_rate: number; // %
    meeting_booking_rate: number; // %
  };
}