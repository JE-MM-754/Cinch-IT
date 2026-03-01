"use client";

import { useCallback, useEffect, useState } from "react";
import { MonthlyPerformanceChart } from "@/components/charts/performance-chart";
import { ModulePageLayout } from "@/components/navigation/module-page-layout";
import { ErrorState } from "@/components/ui/error-state";
import { MetricCardSkeleton, TableSkeleton } from "@/components/ui/loading-skeleton";
import { MetricStatCard } from "@/components/ui/metric-card";
import { Pagination } from "@/components/ui/pagination";
import { SectionTitle } from "@/components/ui/section-title";
import { getDashboardStats, getOutreachEvents } from "@/lib/api";
import type { DashboardStatsResponse, ApiOutreachEvent } from "@/lib/api-types";
import { monthlyPerformance } from "@/lib/demo-data";
import type { MetricCard } from "@/lib/types";

function buildOutreachCards(stats: DashboardStatsResponse): MetricCard[] {
  return [
    { label: "SMS Sent", value: stats.outreach.sms_sent.toLocaleString() },
    { label: "SMS Reply Rate", value: `${(stats.outreach.sms_reply_rate * 100).toFixed(1)}%` },
    { label: "Emails Sent", value: stats.outreach.emails_sent.toLocaleString() },
    { label: "Email Open Rate", value: `${(stats.outreach.email_open_rate * 100).toFixed(1)}%` },
    { label: "Meetings Booked", value: stats.outreach.meetings_booked.toLocaleString() },
    { label: "Overall Reply Rate", value: `${(stats.outreach.overall_reply_rate * 100).toFixed(1)}%` },
  ];
}

export default function ReactivationAnalyticsPage() {
  const [stats, setStats] = useState<DashboardStatsResponse | null>(null);
  const [events, setEvents] = useState<ApiOutreachEvent[]>([]);
  const [loading, setLoading] = useState(true);
  const [eventsLoading, setEventsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [channelFilter, setChannelFilter] = useState("");
  const [page, setPage] = useState(1);
  const [pages, setPages] = useState(1);
  const [total, setTotal] = useState(0);

  const loadStats = useCallback(() => {
    setLoading(true);
    getDashboardStats()
      .then(setStats)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  const loadEvents = useCallback(
    (p: number, channel: string) => {
      setEventsLoading(true);
      getOutreachEvents({ page: p, per_page: 20, channel: channel || undefined })
        .then((res) => {
          setEvents(res.events);
          setPage(res.page);
          setPages(Math.ceil(res.total / res.per_page));
          setTotal(res.total);
        })
        .catch((err) => setError(err.message))
        .finally(() => setEventsLoading(false));
    },
    [],
  );

  useEffect(loadStats, [loadStats]);
  useEffect(() => {
    loadEvents(page, channelFilter);
  }, [page, channelFilter, loadEvents]);

  const handleChannelChange = (value: string) => {
    setChannelFilter(value);
    setPage(1);
  };

  return (
    <ModulePageLayout
      moduleId="reactivation"
      title="Reactivation Analytics"
      description="Analyze campaign effectiveness, response velocity, and pipeline ROI from recovered opportunities."
    >
      {error && <ErrorState message={error} onRetry={() => { loadStats(); loadEvents(page, channelFilter); }} />}

      <section className="rounded-xl border border-slate-800 bg-slate-900/70 p-5">
        <SectionTitle title="Outreach Performance" description="Aggregate metrics across all outreach channels." />
        {loading ? (
          <div className="mt-4 grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
            {Array.from({ length: 6 }).map((_, i) => (
              <MetricCardSkeleton key={i} />
            ))}
          </div>
        ) : stats ? (
          <div className="mt-4 grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
            {buildOutreachCards(stats).map((metric) => (
              <MetricStatCard key={metric.label} metric={metric} />
            ))}
          </div>
        ) : null}
      </section>

      <section className="rounded-xl border border-slate-800 bg-slate-900/70 p-5">
        <SectionTitle title="Recent Outreach Events" description="Individual outreach events with delivery status." />
        <div className="mt-4 flex gap-2">
          {["", "sms", "email"].map((ch) => (
            <button
              key={ch}
              onClick={() => handleChannelChange(ch)}
              className={`rounded-lg border px-3 py-1.5 text-sm transition ${
                channelFilter === ch
                  ? "border-cyan-500 bg-cyan-500/20 text-cyan-200"
                  : "border-slate-700 text-slate-300 hover:border-slate-500"
              }`}
            >
              {ch === "" ? "All" : ch.toUpperCase()}
            </button>
          ))}
        </div>
        {eventsLoading ? (
          <TableSkeleton rows={8} />
        ) : events.length === 0 ? (
          <p className="mt-6 text-center text-sm text-slate-400">No outreach events found.</p>
        ) : (
          <div className="mt-4 overflow-x-auto">
            <table className="min-w-full text-left text-sm">
              <thead className="text-slate-400">
                <tr className="border-b border-slate-800">
                  <th className="px-3 py-2">Channel</th>
                  <th className="px-3 py-2">Status</th>
                  <th className="px-3 py-2">Subject</th>
                  <th className="px-3 py-2">Step</th>
                  <th className="px-3 py-2">Sent</th>
                  <th className="px-3 py-2">Opened</th>
                  <th className="px-3 py-2">Replied</th>
                </tr>
              </thead>
              <tbody>
                {events.map((ev) => (
                  <tr key={ev.id} className="border-b border-slate-900 text-slate-200">
                    <td className="px-3 py-2 uppercase text-cyan-300">{ev.channel}</td>
                    <td className="px-3 py-2 capitalize">{ev.status}</td>
                    <td className="max-w-xs truncate px-3 py-2">{ev.subject || "—"}</td>
                    <td className="px-3 py-2">{ev.sequence_step}</td>
                    <td className="px-3 py-2 text-slate-400">
                      {ev.sent_at ? new Date(ev.sent_at).toLocaleDateString() : "—"}
                    </td>
                    <td className="px-3 py-2 text-slate-400">
                      {ev.opened_at ? new Date(ev.opened_at).toLocaleDateString() : "—"}
                    </td>
                    <td className="px-3 py-2 text-slate-400">
                      {ev.replied_at ? new Date(ev.replied_at).toLocaleDateString() : "—"}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
        <Pagination page={page} pages={pages} total={total} onPageChange={setPage} />
      </section>

      <section className="rounded-xl border border-slate-800 bg-slate-900/70 p-5">
        <SectionTitle
          title="Volume and Conversion"
          description="Qualified opportunities generated from reactivation by month."
        />
        <p className="mt-1 text-xs text-slate-500">Demo data</p>
        <div className="mt-4">
          <MonthlyPerformanceChart data={monthlyPerformance} />
        </div>
      </section>
    </ModulePageLayout>
  );
}
