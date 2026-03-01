"use client";

import { useEffect, useState } from "react";
import { ModulePageLayout } from "@/components/navigation/module-page-layout";
import { SectionTitle } from "@/components/ui/section-title";

interface SequenceStep {
  id: number;
  step_number: number;
  channel: string;
  delay_days: number;
  subject: string;
}

interface Sequence {
  id: number;
  name: string;
  description: string;
  target_segment: string;
  is_active: boolean;
  steps: SequenceStep[];
}

export default function ReactivationSequencesPage() {
  const [sequences, setSequences] = useState<Sequence[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch("/api/sequences")
      .then((res) => {
        if (!res.ok) throw new Error(`API error: ${res.status}`);
        return res.json();
      })
      .then((data) => setSequences(data.sequences))
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  return (
    <ModulePageLayout
      moduleId="reactivation"
      title="Reactivation Sequences"
      description="SMS-first outreach sequences for re-engaging dormant contacts."
    >
      <section className="rounded-xl border border-slate-800 bg-slate-900/70 p-5">
        <SectionTitle
          title="Sequence Library"
          description="Active sequences loaded from the backend."
        />

        {error && (
          <div className="mt-4 rounded-lg border border-rose-500/30 bg-rose-500/10 p-3 text-sm text-rose-300">
            Failed to load sequences: {error}
          </div>
        )}

        <div className="mt-4 grid gap-4 lg:grid-cols-2">
          {loading
            ? Array.from({ length: 3 }).map((_, i) => (
                <div key={i} className="h-40 animate-pulse rounded-xl border border-slate-800 bg-slate-950/70" />
              ))
            : sequences.length === 0
              ? (
                  <p className="col-span-full text-center text-sm text-slate-400 py-6">
                    No sequences created yet. Initialize SMS-first sequences from the backend.
                  </p>
                )
              : sequences.map((seq) => (
                  <article key={seq.id} className="rounded-xl border border-slate-800 bg-slate-950/70 p-4">
                    <div className="flex items-center justify-between">
                      <p className="text-xs uppercase tracking-wide text-cyan-300">
                        {seq.target_segment.replace(/_/g, " ")}
                      </p>
                      <span
                        className={
                          seq.is_active
                            ? "rounded-full bg-emerald-500/20 px-2 py-0.5 text-xs text-emerald-300"
                            : "rounded-full bg-slate-700/50 px-2 py-0.5 text-xs text-slate-400"
                        }
                      >
                        {seq.is_active ? "Active" : "Inactive"}
                      </span>
                    </div>
                    <h3 className="mt-1 text-lg font-semibold text-white">{seq.name}</h3>
                    <p className="mt-1 text-sm text-slate-300">{seq.description}</p>
                    <div className="mt-3 text-sm text-slate-200">
                      <p>Steps: {seq.steps.length}</p>
                    </div>
                    <div className="mt-2 flex flex-wrap gap-1.5">
                      {seq.steps.map((step) => (
                        <span
                          key={step.id}
                          className={
                            step.channel === "sms"
                              ? "rounded border border-cyan-500/30 bg-cyan-500/10 px-2 py-0.5 text-xs text-cyan-300"
                              : "rounded border border-violet-500/30 bg-violet-500/10 px-2 py-0.5 text-xs text-violet-300"
                          }
                        >
                          Day {step.delay_days}: {step.channel.toUpperCase()}
                        </span>
                      ))}
                    </div>
                  </article>
                ))}
        </div>
      </section>
    </ModulePageLayout>
  );
}
