import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Cinch IT — Dead Lead Reactivation",
  description: "AI-powered dead lead reactivation for Cinch IT Boston",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="bg-gray-950 text-gray-100 min-h-screen antialiased">
        <nav className="border-b border-gray-800 bg-gray-900/80 backdrop-blur-sm sticky top-0 z-50">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex items-center justify-between h-16">
              <div className="flex items-center gap-3">
                <span className="text-2xl">🔄</span>
                <div>
                  <h1 className="text-lg font-bold text-white">Dead Lead Reactivation</h1>
                  <p className="text-xs text-gray-400">Cinch IT Boston</p>
                </div>
              </div>
              <div className="flex items-center gap-4">
                <a href="/" className="text-sm text-gray-300 hover:text-white px-3 py-2 rounded-md hover:bg-gray-800 transition">Dashboard</a>
                <a href="/contacts" className="text-sm text-gray-300 hover:text-white px-3 py-2 rounded-md hover:bg-gray-800 transition">Contacts</a>
                <a href="/sequences" className="text-sm text-gray-300 hover:text-white px-3 py-2 rounded-md hover:bg-gray-800 transition">Sequences</a>
                <a href="/outreach" className="text-sm text-gray-300 hover:text-white px-3 py-2 rounded-md hover:bg-gray-800 transition">Outreach</a>
                <a href="/audit" className="text-sm text-gray-300 hover:text-white px-3 py-2 rounded-md hover:bg-gray-800 transition">Audit Log</a>
              </div>
            </div>
          </div>
        </nav>
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {children}
        </main>
      </body>
    </html>
  );
}
