import type { ReactNode } from "react";
import { FooterStatus } from "./footer-status";
import { TopNav } from "./top-nav";

export function AppShell({ children }: { children: ReactNode }) {
  return (
    <div className="min-h-screen flex flex-col">
      <TopNav />
      <main className="flex-1 px-4 sm:px-6 py-8 max-w-5xl mx-auto w-full">{children}</main>
      <FooterStatus />
    </div>
  );
}
