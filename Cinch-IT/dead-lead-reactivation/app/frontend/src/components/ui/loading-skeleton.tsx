export function MetricCardSkeleton() {
  return (
    <div className="rounded-xl border border-slate-800 bg-slate-900/70 p-4">
      <div className="h-3 w-24 animate-pulse rounded bg-slate-800" />
      <div className="mt-3 h-7 w-20 animate-pulse rounded bg-slate-800" />
      <div className="mt-3 h-3 w-32 animate-pulse rounded bg-slate-800" />
    </div>
  );
}

export function TableSkeleton({ rows = 5 }: { rows?: number }) {
  return (
    <div className="mt-4 space-y-3">
      {Array.from({ length: rows }).map((_, i) => (
        <div key={i} className="flex gap-4">
          <div className="h-4 w-32 animate-pulse rounded bg-slate-800" />
          <div className="h-4 w-24 animate-pulse rounded bg-slate-800" />
          <div className="h-4 w-20 animate-pulse rounded bg-slate-800" />
          <div className="h-4 w-16 animate-pulse rounded bg-slate-800" />
          <div className="h-4 w-16 animate-pulse rounded bg-slate-800" />
        </div>
      ))}
    </div>
  );
}

export function CardSkeleton() {
  return (
    <div className="rounded-xl border border-slate-800 bg-slate-950/70 p-4">
      <div className="h-3 w-16 animate-pulse rounded bg-slate-800" />
      <div className="mt-2 h-5 w-48 animate-pulse rounded bg-slate-800" />
      <div className="mt-2 h-3 w-36 animate-pulse rounded bg-slate-800" />
      <div className="mt-3 grid grid-cols-2 gap-2">
        <div className="h-3 w-20 animate-pulse rounded bg-slate-800" />
        <div className="h-3 w-20 animate-pulse rounded bg-slate-800" />
      </div>
    </div>
  );
}
