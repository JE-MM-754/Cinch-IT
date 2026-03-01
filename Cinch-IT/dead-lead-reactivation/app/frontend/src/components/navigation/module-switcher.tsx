"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { ModuleId } from "@/lib/types";
import { cn } from "@/lib/utils";

const modules: { id: ModuleId; label: string; href: string }[] = [
  { id: "reactivation", label: "Dead Lead Reactivation", href: "/reactivation" },
  { id: "prospecting", label: "AI Prospecting", href: "/prospecting" },
  { id: "intelligence", label: "Sales Intelligence", href: "/intelligence" },
];

export function ModuleSwitcher() {
  const pathname = usePathname();

  return (
    <div className="flex flex-wrap gap-2">
      {modules.map((module) => {
        const active = pathname.startsWith(module.href);

        return (
          <Link
            key={module.id}
            href={module.href}
            className={cn(
              "rounded-full border px-3 py-1.5 text-xs font-medium transition",
              active
                ? "border-cyan-500 bg-cyan-500/15 text-cyan-200"
                : "border-slate-700 text-slate-300 hover:border-slate-500 hover:text-white",
            )}
          >
            {module.label}
          </Link>
        );
      })}
    </div>
  );
}
