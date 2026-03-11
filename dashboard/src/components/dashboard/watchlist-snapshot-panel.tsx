import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { SignalBadge } from "@/components/shared/signal-badge";
import { EmptyState } from "@/components/shared/empty-state";
import { formatScore, formatConfidence } from "@/lib/utils";
import { TOOLTIPS } from "@/lib/constants";
import type { WatchlistData } from "@/lib/api/types";

interface WatchlistSnapshotPanelProps {
  data: WatchlistData;
}

export function WatchlistSnapshotPanel({ data }: WatchlistSnapshotPanelProps) {
  if (!data.stocks || data.stocks.length === 0) {
    return (
      <Card>
        <CardHeader>
          <CardTitle className="text-base">Watchlist Snapshot</CardTitle>
        </CardHeader>
        <CardContent>
          <EmptyState
            title="No watchlist data"
            message="Configure your watchlist to see how individual names align with the current frame."
          />
        </CardContent>
      </Card>
    );
  }

  const sorted = [...data.stocks].sort((a, b) => a.rank - b.rank);

  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-base">Watchlist Snapshot</CardTitle>
        <CardDescription>
          How your core names fit the current market frame.
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-border text-xs text-muted-foreground">
                <th className="text-left py-2 pr-3 font-medium">Symbol</th>
                <th className="text-left py-2 pr-3 font-medium">Name</th>
                <th className="text-left py-2 pr-3 font-medium hidden sm:table-cell">Sector</th>
                <th className="text-left py-2 pr-3 font-medium">
                  <span title={TOOLTIPS.alignment}>Alignment</span>
                </th>
                <th className="text-right py-2 pr-3 font-medium">Net Signal</th>
                <th className="text-right py-2 pr-3 font-medium">Confidence</th>
                <th className="text-left py-2 font-medium hidden md:table-cell">Summary</th>
              </tr>
            </thead>
            <tbody>
              {sorted.map((stock) => (
                <tr key={stock.symbol} className="border-b border-border/50 hover:bg-muted/30 transition-colors">
                  <td className="py-2.5 pr-3 font-mono font-semibold text-xs">
                    {stock.symbol}
                  </td>
                  <td className="py-2.5 pr-3 truncate max-w-[140px]">
                    {stock.name}
                  </td>
                  <td className="py-2.5 pr-3 text-muted-foreground hidden sm:table-cell truncate max-w-[100px]">
                    {stock.sector_name}
                  </td>
                  <td className="py-2.5 pr-3">
                    <SignalBadge label={stock.label} />
                  </td>
                  <td className="py-2.5 pr-3 text-right font-mono tabular-nums text-xs">
                    <span
                      className={
                        stock.net_signal > 0
                          ? "text-emerald-400"
                          : stock.net_signal < 0
                            ? "text-rose-400"
                            : "text-muted-foreground"
                      }
                    >
                      {formatScore(stock.net_signal)}
                    </span>
                  </td>
                  <td className="py-2.5 pr-3 text-right text-xs text-muted-foreground tabular-nums">
                    {formatConfidence(stock.confidence)}
                  </td>
                  <td className="py-2.5 text-xs text-muted-foreground hidden md:table-cell">
                    <span className="line-clamp-1 max-w-[220px] inline-block">
                      {stock.explanation}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Summary counts */}
        <div className="flex items-center gap-4 mt-3 pt-3 border-t border-border text-xs text-muted-foreground">
          <span>
            {data.total_stocks} total
          </span>
          <span className="text-emerald-400">
            {data.tailwind_count} tailwind
          </span>
          <span className="text-rose-400">
            {data.headwind_count} headwind
          </span>
          <span className="text-yellow-400">
            {data.mixed_count} mixed
          </span>
        </div>
      </CardContent>
    </Card>
  );
}
