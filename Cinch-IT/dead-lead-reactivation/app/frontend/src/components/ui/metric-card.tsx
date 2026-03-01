import { MetricCard } from "@/lib/types";
import { cn } from "@/lib/utils";

interface MetricCardProps {
  metric: MetricCard;
}

export function MetricStatCard({ metric }: MetricCardProps) {
  return (
    <article className="rounded-xl border border-slate-800 bg-slate-900/70 p-4">
      <p className="text-xs uppercase tracking-wide text-slate-400">{metric.label}</p>
      <p className="mt-2 text-2xl font-semibold text-white">{metric.value}</p>
      <p
        className={cn(
          "mt-2 text-sm font-medium",
          metric.trend === "down"
            ? "text-rose-300"
            : metric.trend === "flat"
              ? "text-slate-300"
              : "text-emerald-300",
        )}
      >
        {metric.delta} vs last 30 days
      </p>
    </article>
  );
}
