import { Link, useLocation } from "react-router-dom";
import { cn } from "@/lib/utils";

const NAV_ITEMS = [
  { label: "Desk", path: "/desk" },
  { label: "Reviews", path: "/reviews" },
  { label: "Rulebook", path: "/rulebook" },
];

export function TopNav() {
  const location = useLocation();

  return (
    <header className="sticky top-0 z-50 border-b bg-background/95 backdrop-blur">
      <div className="flex h-14 items-center px-6 max-w-5xl mx-auto">
        <Link to="/desk" className="mr-8 flex items-center gap-2">
          <span className="text-base font-bold tracking-tight">InvestorFrame Lean</span>
        </Link>

        <nav className="hidden md:flex items-center gap-1">
          {NAV_ITEMS.map((item) => {
            const isActive = location.pathname === item.path;
            return (
              <Link
                key={item.path}
                to={item.path}
                className={cn(
                  "px-3 py-1.5 text-sm rounded-md transition-colors",
                  isActive && "bg-secondary text-foreground font-medium",
                  !isActive && "text-muted-foreground hover:text-foreground hover:bg-secondary/50",
                )}
              >
                {item.label}
              </Link>
            );
          })}
        </nav>

        <div className="ml-auto text-xs text-muted-foreground">
          static-first • no live API
        </div>
      </div>
    </header>
  );
}
