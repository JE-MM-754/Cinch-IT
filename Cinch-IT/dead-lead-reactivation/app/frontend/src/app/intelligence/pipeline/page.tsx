"use client";

import { useMemo, useState } from "react";
import { ModulePageLayout } from "@/components/navigation/module-page-layout";
import { SectionTitle } from "@/components/ui/section-title";
import { pipelineDeals } from "@/lib/demo-data";

export default function IntelligencePipelinePage() {
  const [minConfidence, setMinConfidence] = useState(0);

  const rows = useMemo(
    () => pipelineDeals.filter((deal) => deal.confidence >= minConfidence).sort((a, b) => b.amountK - a.amountK),
    [minConfidence],
  );

  return (
    <ModulePageLayout
      moduleId="intelligence"
      title="Pipeline Health"
      description="Inspect active opportunities by stage, confidence, and projected value."
    >
      <section className="rounded-xl border border-slate-800 bg-slate-900/70 p-5">
        <SectionTitle title="Open Opportunities" description="Sorted by deal size with adjustable confidence threshold." />
        <div className="mt-4 flex flex-wrap items-center gap-3">
          <label className="text-sm text-slate-300" htmlFor="confidence">
            Minimum confidence: {minConfidence}%
          </label>
          <input
            id="confidence"
            type="range"
            min={0}
            max={100}
            value={minConfidence}
            onChange={(event) => setMinConfidence(Number(event.target.value))}
            className="w-56"
          />
        </div>
        <div className="mt-4 overflow-x-auto">
          <table className="min-w-full text-left text-sm">
            <thead className="text-slate-400">
              <tr className="border-b border-slate-800">
                <th className="px-3 py-2">Account</th>
                <th className="px-3 py-2">Stage</th>
                <th className="px-3 py-2">Owner</th>
                <th className="px-3 py-2">Amount ($K)</th>
                <th className="px-3 py-2">Close Date</th>
                <th className="px-3 py-2">Confidence</th>
              </tr>
            </thead>
            <tbody>
              {rows.map((deal) => (
                <tr key={deal.id} className="border-b border-slate-900 text-slate-200">
                  <td className="px-3 py-2 text-white">{deal.account}</td>
                  <td className="px-3 py-2">{deal.stage}</td>
                  <td className="px-3 py-2">{deal.owner}</td>
                  <td className="px-3 py-2">{deal.amountK}</td>
                  <td className="px-3 py-2">{deal.closeDate}</td>
                  <td className="px-3 py-2">{deal.confidence}%</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </ModulePageLayout>
  );
}
