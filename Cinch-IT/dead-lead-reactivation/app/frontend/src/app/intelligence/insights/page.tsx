import { ModulePageLayout } from "@/components/navigation/module-page-layout";
import { SectionTitle } from "@/components/ui/section-title";
import { aiInsights } from "@/lib/demo-data";

export default function IntelligenceInsightsPage() {
  return (
    <ModulePageLayout
      moduleId="intelligence"
      title="AI Insights"
      description="Actionable recommendations generated from activity trends, deal signals, and sequence outcomes."
    >
      <section className="rounded-xl border border-slate-800 bg-slate-900/70 p-5">
        <SectionTitle title="Priority Recommendations" description="Latest insights ranked by projected revenue impact." />
        <div className="mt-4 space-y-3">
          {aiInsights.map((insight) => (
            <article key={insight.id} className="rounded-xl border border-slate-800 bg-slate-950/70 p-4">
              <div className="flex flex-wrap items-center justify-between gap-2">
                <p className="text-base font-semibold text-white">{insight.title}</p>
                <span className="rounded-full border border-slate-700 px-2 py-1 text-xs text-slate-300">{insight.priority}</span>
              </div>
              <p className="mt-2 text-sm text-emerald-300">Impact: {insight.impact}</p>
              <p className="mt-1 text-sm text-slate-300">{insight.recommendation}</p>
            </article>
          ))}
        </div>
      </section>
    </ModulePageLayout>
  );
}
