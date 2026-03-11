import { TopNav } from "./top-nav";
import { FooterStatus } from "./footer-status";

interface AppShellProps {
  children: React.ReactNode;
}

export function AppShell({ children }: AppShellProps) {
  return (
    <div className="min-h-screen flex flex-col">
      <TopNav />
      <main className="flex-1 px-4 sm:px-6 py-6 max-w-[1400px] mx-auto w-full">
        {children}
      </main>
      <FooterStatus />
    </div>
  );
}
