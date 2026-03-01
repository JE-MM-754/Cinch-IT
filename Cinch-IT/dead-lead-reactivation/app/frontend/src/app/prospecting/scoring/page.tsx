import { ModulePageLayout } from "@/components/navigation/module-page-layout";
import { SectionTitle } from "@/components/ui/section-title";

const scoringRules = [
  { rule: "ICP Match: Industry + Headcount", weight: "35%", signal: "Strong in logistics and healthcare" },
  { rule: "Intent Signals: Topic Consumption", weight: "25%", signal: "Pricing page + competitor comparisons" },
  { rule: "Technographic Fit", weight: "20%", signal: "CRM and sequencing stack compatible" },
  { rule: "Buying Committee Accessibility", weight: "20%", signal: "2+ personas reachable" },
];

export default function ScoringPage() {
  return (
    <ModulePageLayout
      moduleId="prospecting"
      title="AI Lead Scoring"
      description="Understand qualification logic and prioritize accounts based on fit, intent, and conversion likelihood."
    >
      <section className="rounded-xl border border-slate-800 bg-slate-900/70 p-5">
        <SectionTitle title="Scoring Framework" description="How the AI model evaluates and ranks leads." />
        <div className="mt-4 overflow-x-auto">
          <table className="min-w-full text-left text-sm">
            <thead className="text-slate-400">
              <tr className="border-b border-slate-800">
                <th className="px-3 py-2">Rule</th>
                <th className="px-3 py-2">Weight</th>
                <th className="px-3 py-2">Current Signal</th>
              </tr>
            </thead>
            <tbody>
              {scoringRules.map((row) => (
                <tr key={row.rule} className="border-b border-slate-900 text-slate-200">
                  <td className="px-3 py-2 text-white">{row.rule}</td>
                  <td className="px-3 py-2">{row.weight}</td>
                  <td className="px-3 py-2">{row.signal}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </ModulePageLayout>
  );
}
