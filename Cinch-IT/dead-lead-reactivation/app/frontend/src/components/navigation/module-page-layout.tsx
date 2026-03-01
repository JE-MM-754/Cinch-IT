import { ReactNode } from "react";
import { ModuleSidebar } from "@/components/navigation/module-sidebar";
import { ModuleId } from "@/lib/types";

interface ModulePageLayoutProps {
  moduleId: ModuleId;
  title: string;
  description: string;
  children: ReactNode;
}

export function ModulePageLayout({ moduleId, title, description, children }: ModulePageLayoutProps) {
  return (
    <div className="space-y-6">
      <header>
        <h1 className="text-3xl font-semibold text-white">{title}</h1>
        <p className="mt-2 max-w-3xl text-sm text-slate-300">{description}</p>
      </header>
      <div className="flex flex-col gap-6 lg:flex-row">
        <ModuleSidebar moduleId={moduleId} />
        <section className="min-w-0 flex-1 space-y-6">{children}</section>
      </div>
    </div>
  );
}
