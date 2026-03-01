import { ModulePageLayout } from "@/components/navigation/module-page-layout";
import { SectionTitle } from "@/components/ui/section-title";
import { sequenceTemplates } from "@/lib/demo-data";

export default function ReactivationSequencesPage() {
  return (
    <ModulePageLayout
      moduleId="reactivation"
      title="Reactivation Sequences"
      description="Use tested playbooks to re-engage dormant contacts with personalized AI messaging."
    >
      <section className="rounded-xl border border-slate-800 bg-slate-900/70 p-5">
        <SectionTitle
          title="Sequence Library"
          description="Performance by template across the last two quarters."
          action="Create Sequence"
        />
        <div className="mt-4 grid gap-4 lg:grid-cols-2">
          {sequenceTemplates.map((template) => (
            <article key={template.id} className="rounded-xl border border-slate-800 bg-slate-950/70 p-4">
              <p className="text-xs uppercase tracking-wide text-cyan-300">{template.id}</p>
              <h3 className="mt-1 text-lg font-semibold text-white">{template.name}</h3>
              <p className="mt-1 text-sm text-slate-300">Audience: {template.audience}</p>
              <div className="mt-3 grid grid-cols-2 gap-2 text-sm text-slate-200">
                <div>Steps: {template.steps}</div>
                <div>Open Rate: {template.openRate}%</div>
                <div>Reply Rate: {template.replyRate}%</div>
                <div>Meetings: {template.meetings}</div>
              </div>
            </article>
          ))}
        </div>
      </section>
    </ModulePageLayout>
  );
}
