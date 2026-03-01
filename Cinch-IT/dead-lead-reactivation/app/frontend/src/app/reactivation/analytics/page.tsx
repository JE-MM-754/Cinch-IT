import { MonthlyPerformanceChart, PipelineValueChart } from "@/components/charts/performance-chart";
import { ModulePageLayout } from "@/components/navigation/module-page-layout";
import { SectionTitle } from "@/components/ui/section-title";
import { monthlyPerformance } from "@/lib/demo-data";

export default function ReactivationAnalyticsPage() {
  return (
    <ModulePageLayout
      moduleId="reactivation"
      title="Reactivation Analytics"
      description="Analyze campaign effectiveness, response velocity, and pipeline ROI from recovered opportunities."
    >
      <section className="rounded-xl border border-slate-800 bg-slate-900/70 p-5">
        <SectionTitle
          title="Volume and Conversion"
          description="Qualified opportunities generated from reactivation by month."
        />
        <div className="mt-4">
          <MonthlyPerformanceChart data={monthlyPerformance} />
        </div>
      </section>
      <section className="rounded-xl border border-slate-800 bg-slate-900/70 p-5">
        <SectionTitle
          title="Pipeline ROI"
          description="Recovered pipeline value across recent months."
        />
        <div className="mt-4">
          <PipelineValueChart data={monthlyPerformance} />
        </div>
      </section>
    </ModulePageLayout>
  );
}
