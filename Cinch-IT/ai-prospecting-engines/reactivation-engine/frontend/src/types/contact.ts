// TypeScript definitions for Cinch IT Reactivation
// Updated by MoneyMachine when backend API changes

export interface Contact {
  id: number;
  first_name: string;
  last_name: string;
  company: string;
  email: string;
  phone: string;
  mobile: string;
  extension: string;
  last_activity: string; // YYYY-MM-DD
  status: 'ready' | 'needs_enrichment' | 'do_not_contact';
  do_not_contact: boolean;
  apollo_enriched: boolean;
  business_verified: boolean;
  current_sequence_step: number;
  last_outreach_at: string | null;
  sms_consent: boolean;
  voice_consent: boolean;
  email_consent: boolean;
  notes: string;
}

export interface OutreachEvent {
  id: number;
  contact_id: number;
  channel: 'email' | 'sms' | 'voice';
  status: string;
  subject: string;
  sequence_step: number;
  sent_at: string | null;
  opened_at: string | null;
  replied_at: string | null;
  response_type: string | null;
  is_test: boolean;
}

export interface DashboardStats {
  contacts: {
    total: number;
    ready: number;
    needs_enrichment: number;
    do_not_contact: number;
    enriched: number;
    sms_ready: number;
    email_only: number;
  };
  outreach: {
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
  };
  test_mode: boolean;
  strategy: string;
}