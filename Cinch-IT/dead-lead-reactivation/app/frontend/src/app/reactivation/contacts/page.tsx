"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { ModulePageLayout } from "@/components/navigation/module-page-layout";
import { ErrorState } from "@/components/ui/error-state";
import { TableSkeleton } from "@/components/ui/loading-skeleton";
import { Pagination } from "@/components/ui/pagination";
import { SectionTitle } from "@/components/ui/section-title";
import { StatusBadge } from "@/components/ui/status-badge";
import { getContacts } from "@/lib/api";
import type { ApiContact } from "@/lib/api-types";

export default function ReactivationContactsPage() {
  const [contacts, setContacts] = useState<ApiContact[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [page, setPage] = useState(1);
  const [pages, setPages] = useState(1);
  const [total, setTotal] = useState(0);
  const [search, setSearch] = useState("");
  const [statusFilter, setStatusFilter] = useState("");
  const debounceRef = useRef<ReturnType<typeof setTimeout>>(undefined);

  const load = useCallback(
    (p: number, q: string, status: string) => {
      setLoading(true);
      setError(null);
      getContacts({ page: p, per_page: 25, search: q || undefined, status: status || undefined })
        .then((res) => {
          setContacts(res.contacts);
          setPage(res.page);
          setPages(res.pages);
          setTotal(res.total);
        })
        .catch((err) => setError(err.message))
        .finally(() => setLoading(false));
    },
    [],
  );

  useEffect(() => {
    load(page, search, statusFilter);
  }, [page, statusFilter, load]);

  const handleSearch = (value: string) => {
    setSearch(value);
    if (debounceRef.current) clearTimeout(debounceRef.current);
    debounceRef.current = setTimeout(() => {
      setPage(1);
      load(1, value, statusFilter);
    }, 300);
  };

  const handleStatusChange = (value: string) => {
    setStatusFilter(value);
    setPage(1);
  };

  return (
    <ModulePageLayout
      moduleId="reactivation"
      title="Contacts"
      description="View and filter contacts from the reactivation pipeline."
    >
      <section className="rounded-xl border border-slate-800 bg-slate-900/70 p-5">
        <SectionTitle
          title="Contact List"
          description="Search and filter contacts by status."
          action="Export Segment"
          actionDisabled
        />
        <div className="mt-4 flex flex-col gap-3 sm:flex-row">
          <input
            value={search}
            onChange={(e) => handleSearch(e.target.value)}
            placeholder="Search name, company, email"
            className="w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-sm text-white outline-none ring-cyan-500 focus:ring"
          />
          <select
            value={statusFilter}
            onChange={(e) => handleStatusChange(e.target.value)}
            className="rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-sm text-slate-200 outline-none ring-cyan-500 focus:ring"
          >
            <option value="">All Statuses</option>
            <option value="ready">Ready</option>
            <option value="needs_enrichment">Needs Enrichment</option>
            <option value="do_not_contact">Do Not Contact</option>
          </select>
        </div>

        {error && (
          <div className="mt-4">
            <ErrorState message={error} onRetry={() => load(page, search, statusFilter)} />
          </div>
        )}

        {loading ? (
          <TableSkeleton rows={10} />
        ) : contacts.length === 0 ? (
          <p className="mt-6 text-center text-sm text-slate-400">No contacts found.</p>
        ) : (
          <div className="mt-4 overflow-x-auto">
            <table className="min-w-full text-left text-sm">
              <thead className="text-slate-400">
                <tr className="border-b border-slate-800">
                  <th className="px-3 py-2">Name</th>
                  <th className="px-3 py-2">Company</th>
                  <th className="px-3 py-2">Email</th>
                  <th className="px-3 py-2">Phone</th>
                  <th className="px-3 py-2">Status</th>
                  <th className="px-3 py-2">SMS Consent</th>
                  <th className="px-3 py-2">Enriched</th>
                </tr>
              </thead>
              <tbody>
                {contacts.map((contact) => (
                  <tr key={contact.id} className="border-b border-slate-900 text-slate-200">
                    <td className="px-3 py-2">
                      <p className="font-medium text-white">
                        {contact.first_name} {contact.last_name}
                      </p>
                    </td>
                    <td className="px-3 py-2">{contact.company}</td>
                    <td className="px-3 py-2 text-slate-300">{contact.email}</td>
                    <td className="px-3 py-2 text-slate-300">{contact.phone || contact.mobile || "—"}</td>
                    <td className="px-3 py-2">
                      <StatusBadge status={contact.status} />
                    </td>
                    <td className="px-3 py-2 text-center">
                      {contact.sms_consent ? (
                        <span className="text-emerald-400">&#10003;</span>
                      ) : (
                        <span className="text-slate-500">&#10005;</span>
                      )}
                    </td>
                    <td className="px-3 py-2 text-center">
                      {contact.apollo_enriched ? (
                        <span className="text-emerald-400">&#10003;</span>
                      ) : (
                        <span className="text-slate-500">&#10005;</span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        <Pagination page={page} pages={pages} total={total} onPageChange={setPage} />
      </section>
    </ModulePageLayout>
  );
}
