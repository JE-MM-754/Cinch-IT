import { ForecastChart } from "@/components/charts/performance-chart";
import { ModulePageLayout } from "@/components/navigation/module-page-layout";
import { SectionTitle } from "@/components/ui/section-title";
import { forecastSeries } from "@/lib/demo-data";

export default function IntelligenceForecastingPage() {
  return (
    <ModulePageLayout
      moduleId="intelligence"
      title="Revenue Forecasting"
      description="Compare commit, best-case, and AI projections to align forecasts and improve planning confidence."
    >
      <section className="rounded-xl border border-slate-800 bg-slate-900/70 p-5">
        <SectionTitle title="Forecast Comparison" description="AI forecast trendline against rep-submitted commit and best-case numbers." />
        <div className="mt-4">
          <ForecastChart data={forecastSeries} />
        </div>
      </section>
    </ModulePageLayout>
  );
}
