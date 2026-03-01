"use client";

import { useCallback, useEffect, useState } from "react";
import { ModulePageLayout } from "@/components/navigation/module-page-layout";
import { SectionTitle } from "@/components/ui/section-title";

interface BackendContact {
  id: number;
  first_name: string;
  last_name: string;
  company: string;
  email: string;
  phone: string;
  mobile: string;
  last_activity: string;
  status: string;
  do_not_contact: boolean;
  sms_consent: boolean;
  current_sequence_step: number;
  last_outreach_at: string | null;
}

export default function ReactivationContactsPage() {
  const [contacts, setContacts] = useState<BackendContact[]>([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [pages, setPages] = useState(1);
  const [query, setQuery] = useState("");
  const [statusFilter, setStatusFilter] = useState("all");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const perPage = 20;

  const fetchContacts = useCallback(() => {
    setLoading(true);
    setError(null);
    const params = new URLSearchParams({
      page: String(page),
      per_page: String(perPage),
    });
    if (query.trim()) params.set("search", query.trim());
    if (statusFilter !== "all") params.set("status", statusFilter);

    fetch(`/api/contacts?${params}`)
      .then((res) => {
        if (!res.ok) throw new Error(`API error: ${res.status}`);
        return res.json();
      })
      .then((data) => {
        setContacts(data.contacts);
        setTotal(data.total);
        setPages(data.pages);
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [page, query, statusFilter]);

  useEffect(() => {
    fetchContacts();
  }, [fetchContacts]);

  // Reset to page 1 when filters change
  useEffect(() => {
    setPage(1);
  }, [query, statusFilter]);

  return (
    <ModulePageLayout
      moduleId="reactivation"
      title="Dormant Contacts"
      description="Browse and manage your dead lead database. All contacts are loaded from the backend."
    >
      <section className="rounded-xl border border-slate-800 bg-slate-900/70 p-5">
        <SectionTitle
          title={`Contact Database (${total.toLocaleString()} total)`}
          description="Search and filter contacts from the real database."
        />
        <div className="mt-4 flex flex-col gap-3 sm:flex-row">
          <input
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            placeholder="Search name, company, email..."
            className="w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-sm text-white outline-none ring-cyan-500 focus:ring"
          />
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-sm text-slate-200"
          >
            <option value="all">All Statuses</option>
            <option value="ready">Ready</option>
            <option value="needs_enrichment">Needs Enrichment</option>
            <option value="do_not_contact">Do Not Contact</option>
          </select>
        </div>

        {error && (
          <div className="mt-4 rounded-lg border border-rose-500/30 bg-rose-500/10 p-3 text-sm text-rose-300">
            Failed to load contacts: {error}
          </div>
        )}

        <div className="mt-4 overflow-x-auto">
          <table className="min-w-full text-left text-sm">
            <thead className="text-slate-400">
              <tr className="border-b border-slate-800">
                <th className="px-3 py-2">Contact</th>
                <th className="px-3 py-2">Company</th>
                <th className="px-3 py-2">Email</th>
                <th className="px-3 py-2">Phone</th>
                <th className="px-3 py-2">Status</th>
                <th className="px-3 py-2">Last Activity</th>
                <th className="px-3 py-2">SMS</th>
              </tr>
            </thead>
            <tbody>
              {loading ? (
                Array.from({ length: 5 }).map((_, i) => (
                  <tr key={i} className="border-b border-slate-900">
                    <td colSpan={7} className="px-3 py-3">
                      <div className="h-4 animate-pulse rounded bg-slate-800" />
                    </td>
                  </tr>
                ))
              ) : contacts.length === 0 ? (
                <tr>
                  <td colSpan={7} className="px-3 py-6 text-center text-slate-400">
                    No contacts found.
                  </td>
                </tr>
              ) : (
                contacts.map((c) => (
                  <tr key={c.id} className="border-b border-slate-900 text-slate-200">
                    <td className="px-3 py-2">
                      <p className="font-medium text-white">
                        {c.first_name} {c.last_name}
                      </p>
                    </td>
                    <td className="px-3 py-2">{c.company}</td>
                    <td className="px-3 py-2 text-xs text-slate-400">{c.email}</td>
                    <td className="px-3 py-2 text-xs text-slate-400">{c.phone || "—"}</td>
                    <td className="px-3 py-2">
                      <span
                        className={
                          c.status === "ready"
                            ? "rounded-full bg-emerald-500/20 px-2 py-0.5 text-xs text-emerald-300"
                            : c.status === "do_not_contact"
                              ? "rounded-full bg-rose-500/20 px-2 py-0.5 text-xs text-rose-300"
                              : "rounded-full bg-amber-500/20 px-2 py-0.5 text-xs text-amber-300"
                        }
                      >
                        {c.status.replace(/_/g, " ")}
                      </span>
                    </td>
                    <td className="px-3 py-2 text-xs text-slate-400">{c.last_activity}</td>
                    <td className="px-3 py-2">
                      {c.sms_consent ? (
                        <span className="text-emerald-400">Yes</span>
                      ) : (
                        <span className="text-slate-500">No</span>
                      )}
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>

        {/* Pagination */}
        {pages > 1 && (
          <div className="mt-4 flex items-center justify-between text-sm">
            <p className="text-slate-400">
              Page {page} of {pages}
            </p>
            <div className="flex gap-2">
              <button
                disabled={page <= 1}
                onClick={() => setPage((p) => Math.max(1, p - 1))}
                className="rounded-lg border border-slate-700 px-3 py-1.5 text-slate-200 transition hover:border-slate-500 disabled:opacity-40"
              >
                Previous
              </button>
              <button
                disabled={page >= pages}
                onClick={() => setPage((p) => Math.min(pages, p + 1))}
                className="rounded-lg border border-slate-700 px-3 py-1.5 text-slate-200 transition hover:border-slate-500 disabled:opacity-40"
              >
                Next
              </button>
            </div>
          </div>
        )}
      </section>
    </ModulePageLayout>
  );
}
