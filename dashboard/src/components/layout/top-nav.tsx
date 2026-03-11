import { Link, useLocation } from "react-router-dom";
import { RefreshCw } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useAppStore } from "@/hooks/use-app-store";
import { useQueryClient } from "@tanstack/react-query";
import { cn } from "@/lib/utils";
import { useState } from "react";

const NAV_ITEMS = [
  { label: "Dashboard", path: "/dashboard" },
  { label: "Scenario Lab", path: "/scenario" },
  { label: "Reports", path: "/reports" },
  { label: "Explain", path: "/explain" },
];

export function TopNav() {
  const location = useLocation();
  const queryClient = useQueryClient();
  const { market, horizon, setMarket, setHorizon } = useAppStore();
  const [isRefreshing, setIsRefreshing] = useState(false);

  const handleRefresh = async () => {
    setIsRefreshing(true);
    await queryClient.invalidateQueries();
    setTimeout(() => setIsRefreshing(false), 600);
  };

  return (
    <header className="sticky top-0 z-50 border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="flex h-14 items-center px-6">
        {/* Brand */}
        <Link to="/dashboard" className="mr-8 flex items-center gap-2">
          <span className="text-base font-bold tracking-tight">InvestorFrame</span>
        </Link>

        {/* Navigation */}
        <nav className="hidden md:flex items-center gap-1">
          {NAV_ITEMS.map((item) => {
            const isActive = location.pathname === item.path;
            const isDisabled = item.path === "/reports" || item.path === "/explain";
            return (
              <Link
                key={item.path}
                to={isDisabled ? "#" : item.path}
                className={cn(
                  "px-3 py-1.5 text-sm rounded-md transition-colors",
                  isActive && "bg-secondary text-foreground font-medium",
                  !isActive && !isDisabled && "text-muted-foreground hover:text-foreground hover:bg-secondary/50",
                  isDisabled && "text-muted-foreground/50 cursor-not-allowed",
                )}
              >
                {item.label}
              </Link>
            );
          })}
        </nav>

        {/* Right controls */}
        <div className="ml-auto flex items-center gap-3">
          <span className="hidden sm:inline text-xs text-muted-foreground bg-amber-500/10 text-amber-400 px-2 py-0.5 rounded">
            Using demo data
          </span>

          <select
            value={market}
            onChange={(e) => setMarket(e.target.value)}
            className="h-8 rounded-md border bg-background px-2 text-xs focus:outline-none focus:ring-1 focus:ring-ring"
          >
            <option value="US">US</option>
          </select>

          <select
            value={horizon}
            onChange={(e) => setHorizon(e.target.value)}
            className="h-8 rounded-md border bg-background px-2 text-xs focus:outline-none focus:ring-1 focus:ring-ring"
          >
            <option value="T+1">T+1</option>
            <option value="T+3">T+3</option>
            <option value="T+5">T+5</option>
            <option value="T+10">T+10</option>
          </select>

          <Button
            variant="ghost"
            size="icon"
            onClick={handleRefresh}
            disabled={isRefreshing}
          >
            <RefreshCw className={cn("h-4 w-4", isRefreshing && "animate-spin")} />
          </Button>
        </div>
      </div>
    </header>
  );
}
