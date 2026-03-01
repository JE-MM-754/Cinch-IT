"use client";

import { useMemo, useState } from "react";
import { ModulePageLayout } from "@/components/navigation/module-page-layout";
import { SectionTitle } from "@/components/ui/section-title";
import { reactivationContacts } from "@/lib/demo-data";

export default function ReactivationContactsPage() {
  const [query, setQuery] = useState("");
  const [sortByScore, setSortByScore] = useState(true);

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    const rows = reactivationContacts.filter((contact) =>
      `${contact.name} ${contact.company} ${contact.title}`.toLowerCase().includes(q),
    );

    return [...rows].sort((a, b) => (sortByScore ? b.potentialScore - a.potentialScore : a.name.localeCompare(b.name)));
  }, [query, sortByScore]);

  return (
    <ModulePageLayout
      moduleId="reactivation"
      title="Dormant Contacts"
      description="Prioritize which dead leads to reactivate using engagement recency, ICP fit, and AI potential scores."
    >
      <section className="rounded-xl border border-slate-800 bg-slate-900/70 p-5">
        <SectionTitle
          title="Contact Queue"
          description="Search and sort contacts before assigning sequences."
          action="Export Segment"
        />
        <div className="mt-4 flex flex-col gap-3 sm:flex-row">
          <input
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            placeholder="Search name, company, title"
            className="w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-sm text-white outline-none ring-cyan-500 focus:ring"
          />
          <button
            onClick={() => setSortByScore((value) => !value)}
            className="rounded-lg border border-slate-700 px-3 py-2 text-sm text-slate-200 hover:border-slate-500 hover:text-white"
          >
            Sort: {sortByScore ? "Potential Score" : "Name"}
          </button>
        </div>
        <div className="mt-4 overflow-x-auto">
          <table className="min-w-full text-left text-sm">
            <thead className="text-slate-400">
              <tr className="border-b border-slate-800">
                <th className="px-3 py-2">Contact</th>
                <th className="px-3 py-2">Company</th>
                <th className="px-3 py-2">Status</th>
                <th className="px-3 py-2">Last Touch</th>
                <th className="px-3 py-2">Score</th>
                <th className="px-3 py-2">Owner</th>
              </tr>
            </thead>
            <tbody>
              {filtered.map((contact) => (
                <tr key={contact.id} className="border-b border-slate-900 text-slate-200">
                  <td className="px-3 py-2">
                    <p className="font-medium text-white">{contact.name}</p>
                    <p className="text-xs text-slate-400">{contact.title}</p>
                  </td>
                  <td className="px-3 py-2">{contact.company}</td>
                  <td className="px-3 py-2 capitalize">{contact.status.replace("-", " ")}</td>
                  <td className="px-3 py-2">{contact.lastTouch}</td>
                  <td className="px-3 py-2">{contact.potentialScore}</td>
                  <td className="px-3 py-2">{contact.owner}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </ModulePageLayout>
  );
}
