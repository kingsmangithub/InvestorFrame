import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { EmptyState } from "@/components/shared/empty-state";
import { AlertTriangle } from "lucide-react";
import { TOOLTIPS } from "@/lib/constants";
import type { MarketData } from "@/lib/api/types";

interface RiskUncertaintyPanelProps {
  data: MarketData;
}

export function RiskUncertaintyPanel({ data }: RiskUncertaintyPanelProps) {
  const bearishEvents = data.active_events.filter(
    (e) => e.direction === "bearish" || e.severity >= 3,
  );

  const riskConditions: string[] = [];

  if (data.regime) {
    if (data.regime.confidence < 0.5) {
      riskConditions.push(
        "Low regime confidence suggests the current classification may be unstable.",
      );
    }

    const highIndicators = Object.entries(data.regime.indicator_values).filter(
      ([, v]) => v >= 0.75,
    );
    for (const [key] of highIndicators) {
      riskConditions.push(
        `Elevated ${key.replace(/_/g, " ")} could shift the regime if it persists or intensifies.`,
      );
    }
  }

  if (data.sentiment && data.sentiment.confidence < 0.5) {
    riskConditions.push(
      "Sentiment confidence is low, meaning the current read may reverse on new information.",
    );
  }

  const hasContent = bearishEvents.length > 0 || riskConditions.length > 0;

  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-base">What Could Break This Frame</CardTitle>
        <CardDescription>{TOOLTIPS.uncertainty}</CardDescription>
      </CardHeader>
      <CardContent>
        {!hasContent ? (
          <EmptyState
            title="No elevated risks detected"
            message="The system has not identified conditions likely to break the current frame. This does not mean risk is absent."
          />
        ) : (
          <ul className="space-y-3">
            {bearishEvents.map((event) => (
              <li key={event.id} className="flex items-start gap-2.5">
                <AlertTriangle className="h-4 w-4 mt-0.5 text-amber-400 flex-shrink-0" />
                <div>
                  <p className="text-sm font-medium">{event.headline}</p>
                  <p className="text-xs text-muted-foreground mt-0.5">
                    Severity {event.severity}/5 &middot;{" "}
                    {event.age_hours < 1
                      ? "< 1 hour ago"
                      : `${Math.round(event.age_hours)}h ago`}
                    {event.subtype && ` \u00B7 ${event.subtype.replace(/_/g, " ")}`}
                  </p>
                </div>
              </li>
            ))}

            {riskConditions.map((condition) => (
              <li key={condition} className="flex items-start gap-2.5">
                <AlertTriangle className="h-4 w-4 mt-0.5 text-amber-400/70 flex-shrink-0" />
                <p className="text-sm text-muted-foreground">{condition}</p>
              </li>
            ))}
          </ul>
        )}
      </CardContent>
    </Card>
  );
}
