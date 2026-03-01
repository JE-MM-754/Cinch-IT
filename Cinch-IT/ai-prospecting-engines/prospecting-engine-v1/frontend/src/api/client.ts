// API client for Cinch IT AI Prospecting Engine
// Use these functions in your components to call the AI backend

const API_BASE = 'http://localhost:8001/api'; // Different port from lead reactivation

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
  getSummary: () => apiCall<ProspectingDashboard>('/dashboard/summary'),
  getLeadFunnel: () => apiCall<any>('/dashboard/lead-funnel'),
  getPerformanceMetrics: () => apiCall<any>('/dashboard/performance'),
};

// Prospect API calls
export const prospects = {
  list: (params: {
    status?: 'hot' | 'warm' | 'cold' | 'disqualified';
    industry?: string;
    search?: string;
    page?: number;
    per_page?: number;
    sort_by?: 'score' | 'created_at' | 'last_activity';
    order?: 'asc' | 'desc';
  } = {}) => {
    const query = new URLSearchParams();
    Object.entries(params).forEach(([key, value]) => {
      if (value) query.append(key, value.toString());
    });
    return apiCall<{
      prospects: Prospect[];
      total: number;
      page: number;
      per_page: number;
      pages: number;
    }>(`/prospects?${query}`);
  },

  get: (id: number) => apiCall<{
    prospect: Prospect;
    ai_analysis: {
      pain_points: string[];
      growth_signals: string[];
      qualification_reasoning: string;
      recommended_approach: string;
    };
    similar_companies: Company[];
  }>(`/prospects/${id}`),

  updateScore: (id: number, updates: {
    human_override?: boolean;
    qualification_status?: 'hot' | 'warm' | 'cold' | 'disqualified';
    notes?: string;
    assigned_to?: string;
  }) => apiCall(`/prospects/${id}/score`, {
    method: 'PATCH',
    body: JSON.stringify(updates),
  }),

  addNote: (id: number, note: string) => apiCall(`/prospects/${id}/notes`, {
    method: 'POST',
    body: JSON.stringify({ note }),
  }),

  bulkQualify: (prospect_ids: number[], action: 'approve' | 'reject' | 'reassign') =>
    apiCall('/prospects/bulk-qualify', {
      method: 'POST',
      body: JSON.stringify({ prospect_ids, action }),
    }),
};

// Campaign API calls
export const campaigns = {
  list: () => apiCall<{ campaigns: Campaign[] }>('/campaigns'),

  get: (id: number) => apiCall<{
    campaign: Campaign;
    prospects: Prospect[];
    performance: CampaignMetrics;
  }>(`/campaigns/${id}`),

  create: (campaign: Omit<Campaign, 'id' | 'created_at' | 'performance_metrics'>) =>
    apiCall('/campaigns', {
      method: 'POST',
      body: JSON.stringify(campaign),
    }),

  start: (id: number) => apiCall(`/campaigns/${id}/start`, { method: 'POST' }),
  
  pause: (id: number) => apiCall(`/campaigns/${id}/pause`, { method: 'POST' }),

  getPerformance: (id: number, timeframe: '7d' | '30d' | '90d' = '30d') =>
    apiCall<CampaignMetrics>(`/campaigns/${id}/performance?timeframe=${timeframe}`),
};

// Outreach API calls
export const outreach = {
  sendTest: (channel: 'email' | 'linkedin', template: string, prospect_id: number) =>
    apiCall('/outreach/test', {
      method: 'POST',
      body: JSON.stringify({ channel, template, prospect_id }),
    }),

  getHistory: (prospect_id: number) => 
    apiCall<{ activities: OutreachActivity[] }>(`/outreach/history/${prospect_id}`),

  classifyResponse: (activity_id: number, response_text: string) =>
    apiCall(`/outreach/classify-response`, {
      method: 'POST',
      body: JSON.stringify({ activity_id, response_text }),
    }),

  bookMeeting: (activity_id: number, meeting_details: {
    date: string;
    time: string;
    duration: number;
    notes?: string;
  }) => apiCall(`/outreach/book-meeting`, {
    method: 'POST',
    body: JSON.stringify({ activity_id, ...meeting_details }),
  }),
};

// Analytics API calls
export const analytics = {
  getProspectingTrends: (timeframe: '30d' | '90d' | '1y' = '30d') =>
    apiCall(`/analytics/prospecting-trends?timeframe=${timeframe}`),

  getIndustryBreakdown: () => apiCall('/analytics/industry-breakdown'),

  getConversionFunnel: (campaign_id?: number) => {
    const query = campaign_id ? `?campaign_id=${campaign_id}` : '';
    return apiCall(`/analytics/conversion-funnel${query}`);
  },

  getRevenueAttribution: () => apiCall('/analytics/revenue-attribution'),

  exportData: (type: 'prospects' | 'campaigns' | 'activities', filters: any = {}) =>
    apiCall(`/analytics/export/${type}`, {
      method: 'POST',
      body: JSON.stringify(filters),
    }),
};

// AI Engine API calls
export const ai = {
  requalifyProspects: (prospect_ids: number[]) =>
    apiCall('/ai/requalify', {
      method: 'POST',
      body: JSON.stringify({ prospect_ids }),
    }),

  generateOutreachContent: (prospect_id: number, message_type: string) =>
    apiCall('/ai/generate-content', {
      method: 'POST',
      body: JSON.stringify({ prospect_id, message_type }),
    }),

  analyzeResponse: (response_text: string, context: {
    prospect_id: number;
    campaign_id: number;
    message_type: string;
  }) => apiCall('/ai/analyze-response', {
    method: 'POST',
    body: JSON.stringify({ response_text, context }),
  }),

  getMarketInsights: (industry?: string, location?: string) => {
    const query = new URLSearchParams();
    if (industry) query.append('industry', industry);
    if (location) query.append('location', location);
    return apiCall(`/ai/market-insights?${query}`);
  },
};

// Admin API calls (for system management)
export const admin = {
  getSystemHealth: () => apiCall('/admin/health'),
  
  getDataSources: () => apiCall('/admin/data-sources'),
  
  updateScrapingConfig: (config: any) => apiCall('/admin/scraping-config', {
    method: 'PUT',
    body: JSON.stringify(config),
  }),

  triggerDataCollection: (source: string, params: any = {}) =>
    apiCall('/admin/trigger-collection', {
      method: 'POST',
      body: JSON.stringify({ source, params }),
    }),
};

// Import types
import type { 
  Prospect, 
  Company, 
  Contact, 
  LeadScore,
  Campaign, 
  CampaignMetrics,
  OutreachActivity,
  ProspectingDashboard 
} from '../types/prospect';