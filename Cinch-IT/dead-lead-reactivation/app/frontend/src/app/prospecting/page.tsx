import { MonthlyPerformanceChart } from "@/components/charts/performance-chart";
import { ModulePageLayout } from "@/components/navigation/module-page-layout";
import { MetricStatCard } from "@/components/ui/metric-card";
import { SectionTitle } from "@/components/ui/section-title";
import { monthlyPerformance, prospectingMetrics } from "@/lib/demo-data";

export default function ProspectingDashboardPage() {
  return (
    <ModulePageLayout
      moduleId="prospecting"
      title="AI Prospecting Dashboard"
      description="Track account discovery, lead qualification, and multi-channel outreach performance."
    >
      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        {prospectingMetrics.map((metric) => (
          <MetricStatCard key={metric.label} metric={metric} />
        ))}
      </div>
      <section className="rounded-xl border border-slate-800 bg-slate-900/70 p-5">
        <SectionTitle title="Top of Funnel Throughput" description="Accounts discovered and leads qualified over six months." />
        <div className="mt-4">
          <MonthlyPerformanceChart data={monthlyPerformance} />
        </div>
      </section>
    </ModulePageLayout>
  );
}
