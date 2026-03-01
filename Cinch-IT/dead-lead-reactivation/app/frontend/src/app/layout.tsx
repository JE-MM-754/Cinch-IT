import type { Metadata } from "next";
import Link from "next/link";
import { ModuleSwitcher } from "@/components/navigation/module-switcher";
import { TestModeBanner } from "@/components/ui/test-mode-banner";
import "./globals.css";

export const metadata: Metadata = {
  title: "Cinch-IT | AI Sales Engine Demo",
  description:
    "Unified multi-module SaaS demo for dead lead reactivation, prospecting, and sales intelligence.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-slate-950 text-slate-100 antialiased">
        <div className="relative min-h-screen overflow-hidden">
          <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_10%_10%,rgba(6,182,212,0.12),transparent_40%),radial-gradient(circle_at_80%_15%,rgba(59,130,246,0.08),transparent_35%),radial-gradient(circle_at_50%_100%,rgba(14,116,144,0.14),transparent_55%)]" />
          <div className="relative z-10">
            <header className="sticky top-0 z-40 border-b border-slate-800 bg-slate-950/90 backdrop-blur">
              <div className="mx-auto flex max-w-7xl flex-col gap-4 px-4 py-4 sm:px-6 lg:px-8">
                <div className="flex flex-wrap items-center justify-between gap-3">
                  <Link href="/" className="flex items-center gap-3">
                    <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-cyan-500/15 text-cyan-300">CI</div>
                    <div>
                      <p className="text-base font-semibold text-white">Cinch-IT AI Sales Engine</p>
                      <p className="text-xs text-slate-400">Live Product Demo Workspace</p>
                    </div>
                  </Link>
                  <div className="rounded-full border border-emerald-500/40 bg-emerald-500/10 px-3 py-1 text-xs font-medium text-emerald-300">
                    Demo Mode Active
                  </div>
                </div>
                <ModuleSwitcher />
              </div>
            </header>
            <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
              <TestModeBanner />
              {children}
            </main>
          </div>
        </div>
      </body>
    </html>
  );
}
