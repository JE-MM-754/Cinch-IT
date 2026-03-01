const statusConfig: Record<string, { label: string; classes: string }> = {
  ready: {
    label: "Ready",
    classes: "border-emerald-500/30 bg-emerald-500/15 text-emerald-300",
  },
  needs_enrichment: {
    label: "Needs Enrichment",
    classes: "border-yellow-500/30 bg-yellow-500/15 text-yellow-300",
  },
  do_not_contact: {
    label: "Do Not Contact",
    classes: "border-rose-500/30 bg-rose-500/15 text-rose-300",
  },
};

export function StatusBadge({ status }: { status: string }) {
  const config = statusConfig[status] ?? {
    label: status,
    classes: "border-slate-500/30 bg-slate-500/15 text-slate-300",
  };

  return (
    <span className={`inline-block rounded-full border px-2 py-0.5 text-xs font-medium ${config.classes}`}>
      {config.label}
    </span>
  );
}
