import type { ReactNode } from "react";
import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import { AppShell } from "@/components/layout/app-shell";
import { DeskPage } from "@/pages/desk-page";
import { HomePage } from "@/pages/home-page";
import { IdeaPage } from "@/pages/idea-page";
import { ReviewsPage } from "@/pages/reviews-page";
import { RulebookPage } from "@/pages/rulebook-page";

function WithShell({ children }: { children: ReactNode }) {
  return <AppShell>{children}</AppShell>;
}

export function AppRouter() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/desk" element={<WithShell><DeskPage /></WithShell>} />
        <Route path="/ideas/:ticker" element={<WithShell><IdeaPage /></WithShell>} />
        <Route path="/reviews" element={<WithShell><ReviewsPage /></WithShell>} />
        <Route path="/rulebook" element={<WithShell><RulebookPage /></WithShell>} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}
