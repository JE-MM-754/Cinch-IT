interface SectionTitleProps {
  title: string;
  description: string;
  action?: string;
  actionDisabled?: boolean;
}

export function SectionTitle({ title, description, action, actionDisabled }: SectionTitleProps) {
  return (
    <div className="flex flex-wrap items-end justify-between gap-2">
      <div>
        <h2 className="text-xl font-semibold text-white">{title}</h2>
        <p className="mt-1 text-sm text-slate-400">{description}</p>
      </div>
      {action ? (
        <button
          disabled={actionDisabled}
          title={actionDisabled ? "Outreach disabled \u2014 coming soon" : undefined}
          className={`rounded-lg border border-slate-700 px-3 py-2 text-sm text-slate-200 transition ${actionDisabled ? "cursor-not-allowed opacity-50" : "hover:border-slate-500 hover:text-white"}`}
        >
          {action}
        </button>
      ) : null}
    </div>
  );
}
