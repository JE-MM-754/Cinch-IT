import { ModulePageLayout } from "@/components/navigation/module-page-layout";
import { SectionTitle } from "@/components/ui/section-title";

const campaigns = [
  { name: "Q2 Enterprise Trigger", channelMix: "Email + LinkedIn", sent: 612, openRate: 49, replyRate: 16 },
  { name: "Ops Leader Winback", channelMix: "Email + Phone", sent: 304, openRate: 55, replyRate: 18 },
  { name: "Healthcare Expansion", channelMix: "LinkedIn + Email", sent: 455, openRate: 52, replyRate: 19 },
];

export default function OutreachPage() {
  return (
    <ModulePageLayout
      moduleId="prospecting"
      title="Outreach Campaigns"
      description="Manage active multi-channel campaigns and monitor engagement performance by segment."
    >
      <section className="rounded-xl border border-slate-800 bg-slate-900/70 p-5">
        <SectionTitle title="Campaign Performance" description="Live campaign metrics from active prospecting cadences." action="Launch Campaign" />
        <div className="mt-4 grid gap-4 md:grid-cols-3">
          {campaigns.map((campaign) => (
            <article key={campaign.name} className="rounded-xl border border-slate-800 bg-slate-950/70 p-4">
              <h3 className="text-base font-semibold text-white">{campaign.name}</h3>
              <p className="mt-1 text-sm text-slate-300">{campaign.channelMix}</p>
              <div className="mt-3 space-y-1 text-sm text-slate-200">
                <p>Sent: {campaign.sent}</p>
                <p>Open Rate: {campaign.openRate}%</p>
                <p>Reply Rate: {campaign.replyRate}%</p>
              </div>
            </article>
          ))}
        </div>
      </section>
    </ModulePageLayout>
  );
}
