"use client";

import { useCallback, useEffect, useState } from "react";
import { ModulePageLayout } from "@/components/navigation/module-page-layout";
import { ErrorState } from "@/components/ui/error-state";
import { CardSkeleton } from "@/components/ui/loading-skeleton";
import { SectionTitle } from "@/components/ui/section-title";
import { getSequences } from "@/lib/api";
import type { ApiSequence } from "@/lib/api-types";

export default function ReactivationSequencesPage() {
  const [sequences, setSequences] = useState<ApiSequence[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [expanded, setExpanded] = useState<Set<number>>(new Set());

  const load = useCallback(() => {
    setLoading(true);
    setError(null);
    getSequences()
      .then((res) => setSequences(res.sequences))
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  useEffect(load, [load]);

  const toggleExpand = (id: number) => {
    setExpanded((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  };

  return (
    <ModulePageLayout
      moduleId="reactivation"
      title="Reactivation Sequences"
      description="View outreach sequence templates and their steps."
    >
      <section className="rounded-xl border border-slate-800 bg-slate-900/70 p-5">
        <SectionTitle
          title="Sequence Library"
          description="Available outreach sequences and their configuration."
          action="Create Sequence"
          actionDisabled
        />

        {error && (
          <div className="mt-4">
            <ErrorState message={error} onRetry={load} />
          </div>
        )}

        {loading ? (
          <div className="mt-4 grid gap-4 lg:grid-cols-2">
            {Array.from({ length: 4 }).map((_, i) => (
              <CardSkeleton key={i} />
            ))}
          </div>
        ) : sequences.length === 0 ? (
          <p className="mt-6 text-center text-sm text-slate-400">No sequences found.</p>
        ) : (
          <div className="mt-4 grid gap-4 lg:grid-cols-2">
            {sequences.map((seq) => (
              <article key={seq.id} className="rounded-xl border border-slate-800 bg-slate-950/70 p-4">
                <div className="flex items-start justify-between gap-2">
                  <div>
                    <p className="text-xs uppercase tracking-wide text-cyan-300">#{seq.id}</p>
                    <h3 className="mt-1 text-lg font-semibold text-white">{seq.name}</h3>
                  </div>
                  <span
                    className={`inline-block rounded-full border px-2 py-0.5 text-xs font-medium ${
                      seq.is_active
                        ? "border-emerald-500/30 bg-emerald-500/15 text-emerald-300"
                        : "border-slate-600/30 bg-slate-600/15 text-slate-400"
                    }`}
                  >
                    {seq.is_active ? "Active" : "Inactive"}
                  </span>
                </div>
                {seq.description && <p className="mt-1 text-sm text-slate-300">{seq.description}</p>}
                <p className="mt-1 text-sm text-slate-400">Target: {seq.target_segment}</p>
                <div className="mt-3 flex items-center justify-between text-sm text-slate-200">
                  <span>{seq.steps.length} step{seq.steps.length !== 1 ? "s" : ""}</span>
                  <button
                    onClick={() => toggleExpand(seq.id)}
                    className="text-xs text-cyan-300 hover:text-cyan-200"
                  >
                    {expanded.has(seq.id) ? "Hide steps" : "Show steps"}
                  </button>
                </div>
                {expanded.has(seq.id) && seq.steps.length > 0 && (
                  <div className="mt-3 space-y-2 border-t border-slate-800 pt-3">
                    {seq.steps.map((step) => (
                      <div key={step.id} className="flex items-start gap-3 text-sm">
                        <span className="mt-0.5 flex h-5 w-5 shrink-0 items-center justify-center rounded-full bg-slate-800 text-xs text-slate-300">
                          {step.step_number}
                        </span>
                        <div>
                          <p className="text-slate-200">
                            <span className="uppercase text-cyan-400">{step.channel}</span>
                            {step.subject && ` — ${step.subject}`}
                          </p>
                          <p className="text-xs text-slate-400">
                            Delay: {step.delay_days} day{step.delay_days !== 1 ? "s" : ""}
                          </p>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
                <div className="mt-3">
                  <button
                    disabled
                    title="Outreach disabled — coming soon"
                    className="w-full cursor-not-allowed rounded-lg border border-slate-700 px-3 py-2 text-sm text-slate-200 opacity-50"
                  >
                    Activate Sequence
                  </button>
                </div>
              </article>
            ))}
          </div>
        )}
      </section>
    </ModulePageLayout>
  );
}
