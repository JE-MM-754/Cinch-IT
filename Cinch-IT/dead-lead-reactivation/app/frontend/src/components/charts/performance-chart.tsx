"use client";

import { useEffect, useState } from "react";
import {
  Bar,
  BarChart,
  CartesianGrid,
  Legend,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { CampaignPerformance, ForecastRecord } from "@/lib/types";

function useChartReady() {
  const [ready, setReady] = useState(false);

  useEffect(() => {
    setReady(true);
  }, []);

  return ready;
}

export function MonthlyPerformanceChart({ data }: { data: CampaignPerformance[] }) {
  const ready = useChartReady();

  if (!ready) {
    return <div className="h-72 w-full rounded-lg border border-slate-800 bg-slate-950/70" />;
  }

  return (
    <div className="h-72 w-full">
      <ResponsiveContainer>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
          <XAxis dataKey="month" stroke="#94a3b8" />
          <YAxis stroke="#94a3b8" />
          <Tooltip />
          <Legend />
          <Bar dataKey="reactivated" name="Reactivated" fill="#22d3ee" radius={[4, 4, 0, 0]} />
          <Bar dataKey="qualified" name="Qualified" fill="#34d399" radius={[4, 4, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

export function PipelineValueChart({ data }: { data: CampaignPerformance[] }) {
  const ready = useChartReady();

  if (!ready) {
    return <div className="h-72 w-full rounded-lg border border-slate-800 bg-slate-950/70" />;
  }

  return (
    <div className="h-72 w-full">
      <ResponsiveContainer>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
          <XAxis dataKey="month" stroke="#94a3b8" />
          <YAxis stroke="#94a3b8" />
          <Tooltip />
          <Line type="monotone" dataKey="pipelineK" name="Pipeline ($K)" stroke="#60a5fa" strokeWidth={3} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

export function ForecastChart({ data }: { data: ForecastRecord[] }) {
  const ready = useChartReady();

  if (!ready) {
    return <div className="h-72 w-full rounded-lg border border-slate-800 bg-slate-950/70" />;
  }

  return (
    <div className="h-72 w-full">
      <ResponsiveContainer>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
          <XAxis dataKey="month" stroke="#94a3b8" />
          <YAxis stroke="#94a3b8" />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="commit" name="Commit ($M)" stroke="#22d3ee" strokeWidth={2} />
          <Line type="monotone" dataKey="bestCase" name="Best Case ($M)" stroke="#f59e0b" strokeWidth={2} />
          <Line type="monotone" dataKey="aiProjection" name="AI Projection ($M)" stroke="#34d399" strokeWidth={3} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
