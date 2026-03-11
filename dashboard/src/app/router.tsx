import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AppShell } from "@/components/layout/app-shell";
import { DashboardPage } from "@/pages/dashboard-page";
import { ScenarioLabPage } from "@/pages/scenario-lab-page";
import { LandingPage } from "@/pages/landing-page";

function WithShell({ children }: { children: React.ReactNode }) {
  return <AppShell>{children}</AppShell>;
}

function ComingSoon({ page }: { page: string }) {
  return (
    <div className="flex flex-col items-center justify-center py-20 text-center">
      <h2 className="text-xl font-semibold">{page}</h2>
      <p className="text-sm text-muted-foreground mt-2">Coming soon.</p>
    </div>
  );
}

export function AppRouter() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Landing page — standalone layout */}
        <Route path="/" element={<LandingPage />} />

        {/* App pages — wrapped in dashboard shell */}
        <Route path="/dashboard" element={<WithShell><DashboardPage /></WithShell>} />
        <Route path="/scenario" element={<WithShell><ScenarioLabPage /></WithShell>} />
        <Route path="/reports" element={<WithShell><ComingSoon page="Reports" /></WithShell>} />
        <Route path="/explain" element={<WithShell><ComingSoon page="Explain" /></WithShell>} />
      </Routes>
    </BrowserRouter>
  );
}
