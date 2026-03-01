import { ForecastChart } from "@/components/charts/performance-chart";
import { ModulePageLayout } from "@/components/navigation/module-page-layout";
import { MetricStatCard } from "@/components/ui/metric-card";
import { SectionTitle } from "@/components/ui/section-title";
import { forecastSeries, intelligenceMetrics } from "@/lib/demo-data";

export default function IntelligenceDashboardPage() {
  return (
    <ModulePageLayout
      moduleId="intelligence"
      title="Sales Intelligence Dashboard"
      description="Track forecast health, deal risk, and AI-driven recommendations for the revenue team."
    >
      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        {intelligenceMetrics.map((metric) => (
          <MetricStatCard key={metric.label} metric={metric} />
        ))}
      </div>
      <section className="rounded-xl border border-slate-800 bg-slate-900/70 p-5">
        <SectionTitle title="Revenue Forecast" description="Commit, best case, and AI-adjusted projection for upcoming months." />
        <div className="mt-4">
          <ForecastChart data={forecastSeries} />
        </div>
      </section>
    </ModulePageLayout>
  );
}
