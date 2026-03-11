import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { RegimeBadge } from "@/components/shared/regime-badge";
import { SentimentGauge } from "@/components/shared/sentiment-gauge";
import { ConfidenceBar } from "@/components/shared/confidence-bar";
import { EmptyState } from "@/components/shared/empty-state";
import { AlertTriangle, TrendingDown } from "lucide-react";
import { TOOLTIPS } from "@/lib/constants";
import type { MarketData } from "@/lib/api/types";

interface MarketFramePanelProps {
  data: MarketData;
}

export function MarketFramePanel({ data }: MarketFramePanelProps) {
  if (!data.regime) {
    return (
      <Card>
        <CardHeader>
          <CardTitle className="text-base">Current Regime</CardTitle>
        </CardHeader>
        <CardContent>
          <EmptyState
            title="Regime unavailable"
            message="No regime classification has been computed."
          />
        </CardContent>
      </Card>
    );
  }

  const { regime, sentiment, active_events } = data;
  const drivers = regime.contributing_factors.slice(0, 5);
  const riskFlags = active_events.filter(
    (e) => e.severity >= 3 && e.direction === "bearish",
  );

  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-base">Current Regime</CardTitle>
        <CardDescription>{TOOLTIPS.regime}</CardDescription>
      </CardHeader>
      <CardContent className="space-y-5">
        {/* Regime badge */}
        <div className="flex items-center gap-3">
          <RegimeBadge regime={regime.state} size="lg" />
        </div>

        {/* Sentiment */}
        {sentiment && (
          <SentimentGauge score={sentiment.composite_score} label={sentiment.label} />
        )}

        {/* Confidence */}
        <ConfidenceBar value={regime.confidence} label="Regime Confidence" />

        {/* Key drivers */}
        {drivers.length > 0 && (
          <div>
            <h4 className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-2">
              Key Drivers
            </h4>
            <ul className="space-y-1.5">
              {drivers.map((factor) => (
                <li key={factor} className="flex items-start gap-2 text-sm">
                  <span className="mt-0.5 h-1.5 w-1.5 rounded-full bg-muted-foreground flex-shrink-0" />
                  <span>{factor}</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Risk flags */}
        {riskFlags.length > 0 && (
          <div>
            <h4 className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-2">
              Risk Flags
            </h4>
            <ul className="space-y-1.5">
              {riskFlags.map((event) => (
                <li key={event.id} className="flex items-start gap-2 text-sm text-rose-400">
                  <TrendingDown className="h-3.5 w-3.5 mt-0.5 flex-shrink-0" />
                  <span>{event.headline}</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Uncertainty caveat */}
        <div className="flex items-start gap-2 rounded-md bg-muted/50 px-3 py-2">
          <AlertTriangle className="h-3.5 w-3.5 mt-0.5 text-amber-400 flex-shrink-0" />
          <p className="text-xs text-muted-foreground">
            {TOOLTIPS.confidence}
          </p>
        </div>
      </CardContent>
    </Card>
  );
}
