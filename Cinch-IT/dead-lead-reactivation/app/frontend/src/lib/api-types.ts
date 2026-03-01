// ─── Health ───
export interface HealthResponse {
  status: string;
  test_mode: boolean;
  env: string;
  version: string;
}

// ─── Dashboard Stats ───
export interface ContactStats {
  total: number;
  ready: number;
  needs_enrichment: number;
  do_not_contact: number;
  enriched: number;
  sms_ready: number;
  email_only: number;
}

export interface OutreachStats {
  total: number;
  sms_sent: number;
  sms_replies: number;
  sms_reply_rate: number;
  emails_sent: number;
  emails_opened: number;
  email_open_rate: number;
  email_replies: number;
  email_reply_rate: number;
  total_replies: number;
  overall_reply_rate: number;
  meetings_booked: number;
}

export interface DashboardStatsResponse {
  contacts: ContactStats;
  outreach: OutreachStats;
  test_mode: boolean;
  strategy: string;
}

// ─── Contacts ───
export interface ApiContact {
  id: number;
  first_name: string;
  last_name: string;
  company: string;
  email: string;
  phone: string;
  mobile: string;
  last_activity: string;
  status: "ready" | "needs_enrichment" | "do_not_contact";
  do_not_contact: boolean;
  apollo_enriched: boolean;
  business_verified: boolean;
  current_sequence_step: number;
  last_outreach_at: string | null;
  sms_consent: boolean;
  voice_consent: boolean;
}

export interface ContactsResponse {
  contacts: ApiContact[];
  total: number;
  page: number;
  per_page: number;
  pages: number;
}

// ─── Sequences ───
export interface SequenceStep {
  id: number;
  step_number: number;
  channel: string;
  delay_days: number;
  subject: string;
}

export interface ApiSequence {
  id: number;
  name: string;
  description: string;
  target_segment: string;
  is_active: boolean;
  steps: SequenceStep[];
}

export interface SequencesResponse {
  sequences: ApiSequence[];
}

// ─── Outreach Events ───
export interface ApiOutreachEvent {
  id: number;
  contact_id: number;
  channel: string;
  status: string;
  subject: string;
  sequence_step: number;
  sent_at: string | null;
  opened_at: string | null;
  replied_at: string | null;
  is_test: boolean;
}

export interface OutreachEventsResponse {
  events: ApiOutreachEvent[];
  total: number;
  page: number;
  per_page: number;
}

// ─── Audit Log ───
export interface ApiAuditLog {
  id: number;
  timestamp: string;
  action: string;
  entity_type: string;
  entity_id: number | null;
  details: Record<string, unknown>;
  user: string;
}

export interface AuditLogResponse {
  logs: ApiAuditLog[];
  total: number;
  page: number;
  per_page: number;
}
