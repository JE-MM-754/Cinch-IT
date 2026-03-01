// API client for Cinch IT backend
// Use these functions in your components to call the backend

const API_BASE = 'http://localhost:8000/api';

export class ApiError extends Error {
  constructor(public status: number, message: string) {
    super(message);
    this.name = 'ApiError';
  }
}

async function apiCall<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const url = `${API_BASE}${endpoint}`;
  const response = await fetch(url, {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  });

  if (!response.ok) {
    throw new ApiError(response.status, `API Error: ${response.statusText}`);
  }

  return response.json();
}

// Dashboard API calls
export const dashboard = {
  getStats: () => apiCall<DashboardStats>('/dashboard/stats'),
};

// Contact API calls  
export const contacts = {
  list: (params: {
    status?: string;
    search?: string;
    page?: number;
    per_page?: number;
  } = {}) => {
    const query = new URLSearchParams();
    Object.entries(params).forEach(([key, value]) => {
      if (value) query.append(key, value.toString());
    });
    return apiCall<{
      contacts: Contact[];
      total: number;
      page: number;
      per_page: number;
      pages: number;
    }>(`/contacts?${query}`);
  },

  get: (id: number) => apiCall<{
    contact: Contact;
    outreach_history: OutreachEvent[];
    meetings: any[];
  }>(`/contacts/${id}`),

  update: (id: number, updates: Partial<Contact>) =>
    apiCall(`/contacts/${id}`, {
      method: 'PATCH',
      body: JSON.stringify(updates),
    }),
};

// Outreach API calls
export const outreach = {
  sendSMS: (contactId: number, body: string, sequenceStep: number = 1) =>
    apiCall(`/outreach/send-sms/${contactId}`, {
      method: 'POST',
      body: JSON.stringify({ body, sequence_step: sequenceStep }),
    }),

  sendEmail: (contactId: number, subject: string, body: string, sequenceStep: number = 1) =>
    apiCall(`/outreach/send-email/${contactId}`, {
      method: 'POST',
      body: JSON.stringify({ subject, body, sequence_step: sequenceStep }),
    }),

  sendTestSMS: (body?: string) =>
    apiCall('/outreach/send-test-sms', {
      method: 'POST',
      body: JSON.stringify({ body }),
    }),

  startSMSBlitz: (limit: number = 10) =>
    apiCall('/outreach/start-sms-blitz', {
      method: 'POST',
      body: JSON.stringify({ limit }),
    }),

  getEvents: (params: {
    channel?: string;
    status?: string;
    page?: number;
    per_page?: number;
  } = {}) => {
    const query = new URLSearchParams();
    Object.entries(params).forEach(([key, value]) => {
      if (value) query.append(key, value.toString());
    });
    return apiCall(`/outreach/events?${query}`);
  },
};

// Import types
import type { Contact, OutreachEvent, DashboardStats } from '../types/contact';