"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { monthlyPerformance } from "@/lib/demo-data";

interface DashboardStats {
  contacts: {
    total: number;
    ready: number;
    sms_ready: number;
  };
  outreach: {
    meetings_booked: number;
    overall_reply_rate: number;
  };
}

export default function Home() {
  const latestMonth = monthlyPerformance[monthlyPerformance.length - 1];
  const [stats, setStats] = useState<DashboardStats | null>(null);

  useEffect(() => {
    fetch("/api/dashboard/stats")
      .then((res) => (res.ok ? res.json() : null))
      .then(setStats)
      .catch(() => {});
  }, []);

  const reactivationStats = stats
    ? [
        `${stats.contacts.total.toLocaleString()} contacts loaded`,
        `${stats.contacts.sms_ready.toLocaleString()} SMS-ready`,
        `${stats.contacts.ready.toLocaleString()} ready for outreach`,
      ]
    : ["Loading...", "", ""];

  const modules = [
    {
      title: "Dead Lead Reactivation",
      href: "/reactivation",
      summary: "Recover dormant opportunities with AI sequence orchestration and behavior-triggered follow-up.",
      stats: reactivationStats,
    },
    {
      title: "AI Prospecting Engine",
      href: "/prospecting",
      summary: "Discover and qualify new accounts with intent signals, ICP scoring, and channel recommendations.",
      stats: ["2,381 accounts discovered", "684 AI-qualified leads", "18.6% reply rate"],
    },
    {
      title: "Sales Intelligence",
      href: "/intelligence",
      summary: "Forecast accurately, surface deal risks early, and guide revenue execution with AI insights.",
      stats: ["93% forecast accuracy", "3.7x pipeline coverage", "$6.8M Q2 projection"],
    },
  ];

  return (
    <div className="space-y-8">
      <section className="rounded-2xl border border-slate-800 bg-slate-900/70 p-8">
        <p className="text-xs uppercase tracking-[0.2em] text-cyan-300">Unified Platform</p>
        <h1 className="mt-3 text-4xl font-semibold text-white">AI Sales Engine Demo</h1>
        <p className="mt-3 max-w-3xl text-slate-300">
          This workspace simulates a full revenue automation workflow from dormant lead recovery to new prospect discovery and AI-driven forecast decisions.
        </p>
        <div className="mt-6 grid gap-3 text-sm text-slate-200 sm:grid-cols-3">
          <div className="rounded-xl border border-slate-700 bg-slate-800/50 p-4">Import leads and enrich firmographics</div>
          <div className="rounded-xl border border-slate-700 bg-slate-800/50 p-4">Launch personalized multi-channel outreach</div>
          <div className="rounded-xl border border-slate-700 bg-slate-800/50 p-4">Track pipeline lift and forecast confidence</div>
        </div>
      </section>

      <section className="grid gap-5 lg:grid-cols-3">
        {modules.map((module) => (
          <article key={module.title} className="rounded-xl border border-slate-800 bg-slate-900/70 p-6">
            <h2 className="text-xl font-semibold text-white">{module.title}</h2>
            <p className="mt-2 text-sm text-slate-300">{module.summary}</p>
            <ul className="mt-4 space-y-1 text-sm text-slate-200">
              {module.stats.filter(Boolean).map((stat) => (
                <li key={stat}>{stat}</li>
              ))}
            </ul>
            <Link
              href={module.href}
              className="mt-5 inline-flex rounded-lg border border-cyan-500/50 bg-cyan-500/10 px-4 py-2 text-sm font-medium text-cyan-200 transition hover:bg-cyan-500/20"
            >
              Open Module
            </Link>
          </article>
        ))}
      </section>

      <section className="grid gap-5 lg:grid-cols-2">
        <article className="rounded-xl border border-slate-800 bg-slate-900/70 p-6">
          <h2 className="text-xl font-semibold text-white">Last 30 Days Snapshot</h2>
          <p className="mt-2 text-sm text-slate-300">
            {latestMonth.reactivated} dormant contacts reactivated, {latestMonth.qualified} qualified opportunities, and ${latestMonth.pipelineK}K generated pipeline.
          </p>
        </article>
        <article className="rounded-xl border border-slate-800 bg-slate-900/70 p-6">
          <h2 className="text-xl font-semibold text-white">Demo Narrative</h2>
          <p className="mt-2 text-sm text-slate-300">
            Use the module switcher to walk prospects through an end-to-end AI sales operating system: identify targets, execute outreach, and act on intelligence.
          </p>
        </article>
      </section>
    </div>
  );
}
