"use client";

import { useCallback, useEffect, useState } from "react";
import { ModulePageLayout } from "@/components/navigation/module-page-layout";
import { ErrorState } from "@/components/ui/error-state";
import { CardSkeleton } from "@/components/ui/loading-skeleton";
import { Pagination } from "@/components/ui/pagination";
import { SectionTitle } from "@/components/ui/section-title";
import { getAuditLog } from "@/lib/api";
import type { ApiAuditLog } from "@/lib/api-types";

function formatDetails(details: Record<string, unknown>): string {
  const entries = Object.entries(details);
  if (entries.length === 0) return "";
  return entries.map(([k, v]) => `${k}: ${String(v)}`).join(", ");
}

export default function ReactivationAuditLogPage() {
  const [logs, setLogs] = useState<ApiAuditLog[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [page, setPage] = useState(1);
  const [pages, setPages] = useState(1);
  const [total, setTotal] = useState(0);

  const load = useCallback(
    (p: number) => {
      setLoading(true);
      setError(null);
      getAuditLog({ page: p, per_page: 25 })
        .then((res) => {
          setLogs(res.logs);
          setPage(res.page);
          setPages(Math.ceil(res.total / res.per_page));
          setTotal(res.total);
        })
        .catch((err) => setError(err.message))
        .finally(() => setLoading(false));
    },
    [],
  );

  useEffect(() => {
    load(page);
  }, [page, load]);

  return (
    <ModulePageLayout
      moduleId="reactivation"
      title="Audit Log"
      description="Transparent timeline of system actions, outreach events, and automation decisions."
    >
      <section className="rounded-xl border border-slate-800 bg-slate-900/70 p-5">
        <SectionTitle title="Activity Log" description="Chronological feed of system actions and outcomes." />

        {error && (
          <div className="mt-4">
            <ErrorState message={error} onRetry={() => load(page)} />
          </div>
        )}

        {loading ? (
          <div className="mt-4 space-y-3">
            {Array.from({ length: 6 }).map((_, i) => (
              <CardSkeleton key={i} />
            ))}
          </div>
        ) : logs.length === 0 ? (
          <p className="mt-6 text-center text-sm text-slate-400">No audit log entries found.</p>
        ) : (
          <div className="mt-4 space-y-3">
            {logs.map((log) => (
              <article key={log.id} className="rounded-lg border border-slate-800 bg-slate-950/70 p-4">
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <p className="text-sm font-medium text-white">{log.action}</p>
                  <p className="text-xs text-slate-400">
                    {new Date(log.timestamp).toLocaleString()}
                  </p>
                </div>
                <div className="mt-2 flex flex-wrap gap-x-4 gap-y-1 text-sm">
                  <p className="text-slate-300">User: {log.user}</p>
                  {log.entity_type && (
                    <p className="text-slate-400">
                      {log.entity_type}
                      {log.entity_id != null ? ` #${log.entity_id}` : ""}
                    </p>
                  )}
                </div>
                {log.details && Object.keys(log.details).length > 0 && (
                  <p className="mt-1 text-sm text-emerald-300">{formatDetails(log.details)}</p>
                )}
              </article>
            ))}
          </div>
        )}

        <Pagination page={page} pages={pages} total={total} onPageChange={setPage} />
      </section>
    </ModulePageLayout>
  );
}
