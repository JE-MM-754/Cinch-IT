interface SectionTitleProps {
  title: string;
  description: string;
  action?: string;
}

export function SectionTitle({ title, description, action }: SectionTitleProps) {
  return (
    <div className="flex flex-wrap items-end justify-between gap-2">
      <div>
        <h2 className="text-xl font-semibold text-white">{title}</h2>
        <p className="mt-1 text-sm text-slate-400">{description}</p>
      </div>
      {action ? (
        <button className="rounded-lg border border-slate-700 px-3 py-2 text-sm text-slate-200 transition hover:border-slate-500 hover:text-white">
          {action}
        </button>
      ) : null}
    </div>
  );
}
