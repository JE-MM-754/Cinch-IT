import { ModulePageLayout } from "@/components/navigation/module-page-layout";
import { SectionTitle } from "@/components/ui/section-title";
import { auditLog } from "@/lib/demo-data";

export default function ReactivationAuditLogPage() {
  return (
    <ModulePageLayout
      moduleId="reactivation"
      title="Reactivation Audit Log"
      description="Transparent timeline of AI actions, sequence events, and automation decisions for compliance and trust."
    >
      <section className="rounded-xl border border-slate-800 bg-slate-900/70 p-5">
        <SectionTitle title="Recent Automation Activity" description="Chronological feed of system actions and outcomes." />
        <div className="mt-4 space-y-3">
          {auditLog.map((event) => (
            <article key={`${event.time}-${event.action}`} className="rounded-lg border border-slate-800 bg-slate-950/70 p-4">
              <div className="flex flex-wrap items-center justify-between gap-2">
                <p className="text-sm font-medium text-white">{event.action}</p>
                <p className="text-xs text-slate-400">{event.time}</p>
              </div>
              <p className="mt-2 text-sm text-slate-300">Actor: {event.actor}</p>
              <p className="mt-1 text-sm text-emerald-300">Result: {event.result}</p>
            </article>
          ))}
        </div>
      </section>
    </ModulePageLayout>
  );
}
