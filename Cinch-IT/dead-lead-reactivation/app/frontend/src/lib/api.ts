import type {
  HealthResponse,
  DashboardStatsResponse,
  ContactsResponse,
  SequencesResponse,
  OutreachEventsResponse,
  AuditLogResponse,
} from "./api-types";

export class ApiError extends Error {
  constructor(
    public status: number,
    message: string,
  ) {
    super(message);
    this.name = "ApiError";
  }
}

async function fetchApi<T>(path: string, params?: Record<string, string>): Promise<T> {
  const url = new URL(path, window.location.origin);
  if (params) {
    for (const [k, v] of Object.entries(params)) {
      if (v !== undefined && v !== "") url.searchParams.set(k, v);
    }
  }
  const res = await fetch(url.toString());
  if (!res.ok) {
    throw new ApiError(res.status, `API error: ${res.status} ${res.statusText}`);
  }
  return res.json() as Promise<T>;
}

export async function getHealth(): Promise<HealthResponse> {
  return fetchApi<HealthResponse>("/api/health");
}

export async function getDashboardStats(): Promise<DashboardStatsResponse> {
  return fetchApi<DashboardStatsResponse>("/api/dashboard/stats");
}

export async function getContacts(params?: {
  status?: string;
  search?: string;
  page?: number;
  per_page?: number;
}): Promise<ContactsResponse> {
  const p: Record<string, string> = {};
  if (params?.status) p.status = params.status;
  if (params?.search) p.search = params.search;
  if (params?.page) p.page = String(params.page);
  if (params?.per_page) p.per_page = String(params.per_page);
  return fetchApi<ContactsResponse>("/api/contacts", p);
}

export async function getSequences(): Promise<SequencesResponse> {
  return fetchApi<SequencesResponse>("/api/sequences");
}

export async function getOutreachEvents(params?: {
  channel?: string;
  status?: string;
  page?: number;
  per_page?: number;
}): Promise<OutreachEventsResponse> {
  const p: Record<string, string> = {};
  if (params?.channel) p.channel = params.channel;
  if (params?.status) p.status = params.status;
  if (params?.page) p.page = String(params.page);
  if (params?.per_page) p.per_page = String(params.per_page);
  return fetchApi<OutreachEventsResponse>("/api/outreach/events", p);
}

export async function getAuditLog(params?: {
  page?: number;
  per_page?: number;
}): Promise<AuditLogResponse> {
  const p: Record<string, string> = {};
  if (params?.page) p.page = String(params.page);
  if (params?.per_page) p.per_page = String(params.per_page);
  return fetchApi<AuditLogResponse>("/api/audit", p);
}
