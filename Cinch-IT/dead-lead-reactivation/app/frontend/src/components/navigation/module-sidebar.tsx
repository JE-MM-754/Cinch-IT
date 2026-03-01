"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { moduleNavigation, moduleSummary } from "@/lib/demo-data";
import { ModuleId } from "@/lib/types";
import { cn } from "@/lib/utils";

interface ModuleSidebarProps {
  moduleId: ModuleId;
}

export function ModuleSidebar({ moduleId }: ModuleSidebarProps) {
  const pathname = usePathname();
  const summary = moduleSummary[moduleId];

  return (
    <aside className="w-full rounded-xl border border-slate-800 bg-slate-900/75 p-4 lg:w-72 lg:min-h-[calc(100vh-10rem)]">
      <p className="text-xs uppercase tracking-[0.2em] text-cyan-300">Module</p>
      <h2 className="mt-1 text-lg font-semibold text-white">{summary.name}</h2>
      <p className="mt-2 text-sm text-slate-400">{summary.subtitle}</p>
      <nav className="mt-5 space-y-1">
        {moduleNavigation[moduleId].map((item) => {
          const active = pathname === item.href;

          return (
            <Link
              key={item.href}
              href={item.href}
              className={cn(
                "block rounded-lg px-3 py-2 text-sm transition",
                active
                  ? "bg-slate-700 text-white"
                  : "text-slate-300 hover:bg-slate-800 hover:text-white",
              )}
            >
              {item.label}
            </Link>
          );
        })}
      </nav>
    </aside>
  );
}
