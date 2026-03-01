"use client";

import { useEffect, useState } from "react";
import { AlertTriangle } from "lucide-react";
import { getHealth } from "@/lib/api";

export function TestModeBanner() {
  const [testMode, setTestMode] = useState(false);

  useEffect(() => {
    getHealth()
      .then((h) => setTestMode(h.test_mode))
      .catch(() => {});
  }, []);

  if (!testMode) return null;

  return (
    <div className="mb-6 rounded-lg border border-yellow-500/40 bg-yellow-500/10 px-4 py-3">
      <div className="flex items-center gap-2">
        <AlertTriangle className="h-4 w-4 shrink-0 text-yellow-400" />
        <p className="text-sm font-medium text-yellow-300">
          Test Mode Active — No real messages will be sent
        </p>
      </div>
    </div>
  );
}
