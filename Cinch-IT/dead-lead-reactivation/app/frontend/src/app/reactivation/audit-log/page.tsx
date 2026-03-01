"use client";

import { useEffect, useState } from "react";
import { ModulePageLayout } from "@/components/navigation/module-page-layout";
import { SectionTitle } from "@/components/ui/section-title";

interface AuditEntry {
  id: number;
  timestamp: string;
  action: string;
  entity_type: string | null;
  entity_id: number | null;
  details: Record<string, unknown> | null;
  user: string;
}

export default function ReactivationAuditLogPage() {
  const [logs, setLogs] = useState<AuditEntry[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch("/api/audit?per_page=50")
      .then((res) => {
        if (!res.ok) throw new Error(`API error: ${res.status}`);
        return res.json();
      })
      .then((data) => setLogs(data.logs))
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  function formatTimestamp(ts: string) {
    const date = new Date(ts);
    return date.toLocaleString("en-US", {
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  }

  function formatDetails(details: Record<string, unknown> | null): string {
    if (!details) return "";
    if (typeof details === "string") return details;
    // Show a compact summary of the details object
    const entries = Object.entries(details);
    return entries.map(([k, v]) => {
      if (typeof v === "object" && v !== null) return `${k}: ${JSON.stringify(v)}`;
      return `${k}: ${v}`;
    }).join(" | ");
  }

  return (
    <ModulePageLayout
      moduleId="reactivation"
      title="Reactivation Audit Log"
      description="Transparent timeline of system actions, imports, and automation events for compliance and trust."
    >
      <section className="rounded-xl border border-slate-800 bg-slate-900/70 p-5">
        <SectionTitle title="System Activity Log" description="Events loaded from the backend audit trail." />

        {error && (
          <div className="mt-4 rounded-lg border border-rose-500/30 bg-rose-500/10 p-3 text-sm text-rose-300">
            Failed to load audit log: {error}
          </div>
        )}

        <div className="mt-4 space-y-3">
          {loading ? (
            Array.from({ length: 3 }).map((_, i) => (
              <div key={i} className="h-20 animate-pulse rounded-lg border border-slate-800 bg-slate-950/70" />
            ))
          ) : logs.length === 0 ? (
            <p className="py-6 text-center text-sm text-slate-400">No audit log entries yet.</p>
          ) : (
            logs.map((entry) => (
              <article key={entry.id} className="rounded-lg border border-slate-800 bg-slate-950/70 p-4">
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <p className="text-sm font-medium text-white">
                    {entry.action.replace(/_/g, " ")}
                  </p>
                  <p className="text-xs text-slate-400">{formatTimestamp(entry.timestamp)}</p>
                </div>
                <p className="mt-2 text-sm text-slate-300">
                  Actor: {entry.user}
                  {entry.entity_type && (
                    <span className="ml-3 text-slate-400">
                      Entity: {entry.entity_type}
                      {entry.entity_id != null && ` #${entry.entity_id}`}
                    </span>
                  )}
                </p>
                {entry.details && (
                  <p className="mt-1 text-xs text-slate-400 break-all">
                    {formatDetails(entry.details)}
                  </p>
                )}
              </article>
            ))
          )}
        </div>
      </section>
    </ModulePageLayout>
  );
}
