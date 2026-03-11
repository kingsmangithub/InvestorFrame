import { ArrowUpRight, ArrowDownRight, Minus } from "lucide-react";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";
import { formatDelta } from "@/lib/utils";
import type { ScenarioData, ScenarioStockDelta } from "@/lib/api/types";

interface ScenarioWatchlistImpactProps {
  data: ScenarioData;
}

const MIXED_THRESHOLD = 10;

function StockRow({ stock }: { stock: ScenarioStockDelta }) {
  const isPositive = stock.delta > 0;
  const isMixed = Math.abs(stock.delta) < MIXED_THRESHOLD;

  return (
    <div className="flex items-center justify-between gap-2 rounded-md bg-muted/30 px-3 py-2">
      <div className="min-w-0">
        <p className="text-sm font-medium text-foreground truncate">
          {stock.symbol}
        </p>
        <p className="text-xs text-muted-foreground truncate">{stock.name}</p>
      </div>
      <div className="flex items-center gap-2 shrink-0">
        <span
          className={cn(
            "text-sm font-medium tabular-nums",
            isMixed
              ? "text-muted-foreground"
              : isPositive
                ? "text-emerald-400"
                : "text-rose-400",
          )}
        >
          {formatDelta(stock.delta)}
        </span>
        {stock.label_change && (
          <Badge
            variant="outline"
            className="text-[10px] px-1.5 py-0 border-amber-500/30 text-amber-400"
          >
            {stock.label_change}
          </Badge>
        )}
      </div>
    </div>
  );
}

function StockColumn({
  title,
  icon,
  stocks,
  accentClass,
}: {
  title: string;
  icon: React.ReactNode;
  stocks: ScenarioStockDelta[];
  accentClass: string;
}) {
  if (stocks.length === 0) return null;

  return (
    <div className="space-y-2">
      <div className={cn("flex items-center gap-1.5 text-xs font-medium", accentClass)}>
        {icon}
        {title}
        <span className="text-muted-foreground font-normal">({stocks.length})</span>
      </div>
      <div className="space-y-1.5">
        {stocks.map((stock) => (
          <StockRow key={stock.symbol} stock={stock} />
        ))}
      </div>
    </div>
  );
}

export function ScenarioWatchlistImpact({ data }: ScenarioWatchlistImpactProps) {
  const stocks = data.watchlist_impacts ?? [];

  if (stocks.length === 0) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Watchlist Impact</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-muted-foreground">
            No watchlist impact data available for this scenario.
          </p>
        </CardContent>
      </Card>
    );
  }

  const beneficiaries = stocks.filter(
    (s) => s.delta >= MIXED_THRESHOLD,
  );
  const pressured = stocks.filter(
    (s) => s.delta <= -MIXED_THRESHOLD,
  );
  const mixed = stocks.filter(
    (s) => Math.abs(s.delta) < MIXED_THRESHOLD,
  );

  return (
    <Card>
      <CardHeader>
        <CardTitle>Watchlist Impact</CardTitle>
        <CardDescription>
          How individual watchlist names respond under this simulated scenario.
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="grid gap-5 md:grid-cols-3">
          <StockColumn
            title="Beneficiaries"
            icon={<ArrowUpRight className="h-3.5 w-3.5" />}
            stocks={beneficiaries}
            accentClass="text-emerald-400"
          />
          <StockColumn
            title="Pressured Names"
            icon={<ArrowDownRight className="h-3.5 w-3.5" />}
            stocks={pressured}
            accentClass="text-rose-400"
          />
          <StockColumn
            title="Mixed Names"
            icon={<Minus className="h-3.5 w-3.5" />}
            stocks={mixed}
            accentClass="text-muted-foreground"
          />
        </div>
      </CardContent>
    </Card>
  );
}
