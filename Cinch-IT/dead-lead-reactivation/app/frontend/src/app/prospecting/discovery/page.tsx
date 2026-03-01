"use client";

import { useMemo, useState } from "react";
import { ModulePageLayout } from "@/components/navigation/module-page-layout";
import { SectionTitle } from "@/components/ui/section-title";
import { discoveredLeads } from "@/lib/demo-data";

export default function DiscoveryPage() {
  const [intentFilter, setIntentFilter] = useState<"all" | "high" | "medium" | "low">("all");

  const rows = useMemo(() => {
    const filtered =
      intentFilter === "all"
        ? discoveredLeads
        : discoveredLeads.filter((lead) => lead.intent === intentFilter);

    return [...filtered].sort((a, b) => b.fitScore - a.fitScore);
  }, [intentFilter]);

  return (
    <ModulePageLayout
      moduleId="prospecting"
      title="Lead Discovery"
      description="Filter newly discovered accounts by buying intent and ICP fit to prioritize outreach."
    >
      <section className="rounded-xl border border-slate-800 bg-slate-900/70 p-5">
        <SectionTitle title="Discovered Accounts" description="AI-ranked leads sourced from intent and firmographic signals." />
        <div className="mt-4 flex flex-wrap gap-2">
          {(["all", "high", "medium", "low"] as const).map((intent) => (
            <button
              key={intent}
              onClick={() => setIntentFilter(intent)}
              className={`rounded-full border px-3 py-1 text-xs uppercase tracking-wide ${
                intentFilter === intent
                  ? "border-cyan-500 bg-cyan-500/20 text-cyan-200"
                  : "border-slate-700 text-slate-300"
              }`}
            >
              {intent}
            </button>
          ))}
        </div>
        <div className="mt-4 overflow-x-auto">
          <table className="min-w-full text-left text-sm">
            <thead className="text-slate-400">
              <tr className="border-b border-slate-800">
                <th className="px-3 py-2">Company</th>
                <th className="px-3 py-2">Contact</th>
                <th className="px-3 py-2">Fit Score</th>
                <th className="px-3 py-2">Intent</th>
                <th className="px-3 py-2">Channel</th>
                <th className="px-3 py-2">Stage</th>
              </tr>
            </thead>
            <tbody>
              {rows.map((lead) => (
                <tr key={lead.id} className="border-b border-slate-900 text-slate-200">
                  <td className="px-3 py-2 text-white">{lead.company}</td>
                  <td className="px-3 py-2">{lead.contact}</td>
                  <td className="px-3 py-2">{lead.fitScore}</td>
                  <td className="px-3 py-2 capitalize">{lead.intent}</td>
                  <td className="px-3 py-2">{lead.channel}</td>
                  <td className="px-3 py-2 capitalize">{lead.stage}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </ModulePageLayout>
  );
}
