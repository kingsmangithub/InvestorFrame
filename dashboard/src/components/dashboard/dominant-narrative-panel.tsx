import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { EmptyState } from "@/components/shared/empty-state";
import { BookOpen } from "lucide-react";
import { TOOLTIPS } from "@/lib/constants";
import type { MarketData } from "@/lib/api/types";

interface DominantNarrativePanelProps {
  data: MarketData;
}

function buildNarrativeExplanation(data: MarketData): string {
  const parts: string[] = [];

  if (data.regime) {
    parts.push(
      `The current market frame is classified as ${data.regime.state.replace(/_/g, " ")}, driven primarily by ${data.regime.contributing_factors.slice(0, 2).join(" and ").toLowerCase() || "broad macro conditions"}.`,
    );
  }

  if (data.sentiment) {
    parts.push(
      `Composite sentiment reads ${data.sentiment.label.replace(/_/g, " ")} at ${data.sentiment.composite_score.toFixed(1)}, suggesting the weight of evidence ${data.sentiment.composite_score >= 0 ? "leans constructive" : "leans cautious"}.`,
    );
  }

  if (data.active_events.length > 1) {
    const highSeverity = data.active_events.filter((e) => e.severity >= 3);
    if (highSeverity.length > 0) {
      parts.push(
        `${highSeverity.length} notable event${highSeverity.length > 1 ? "s" : ""} may be shaping near-term positioning.`,
      );
    }
  }

  return parts.length > 0
    ? parts.join(" ")
    : "Insufficient data to construct a narrative summary.";
}

export function DominantNarrativePanel({ data }: DominantNarrativePanelProps) {
  const topEvent = data.active_events.length > 0
    ? data.active_events.reduce((a, b) => (a.severity >= b.severity ? a : b))
    : null;

  if (!topEvent && !data.regime) {
    return (
      <Card>
        <CardHeader>
          <CardTitle className="text-base">Dominant Narrative</CardTitle>
        </CardHeader>
        <CardContent>
          <EmptyState
            title="No narrative available"
            message="Event and regime data required to construct a narrative."
          />
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-base">Dominant Narrative</CardTitle>
        <CardDescription>{TOOLTIPS.dominantNarrative}</CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        {/* Headline */}
        {topEvent && (
          <div className="flex items-start gap-2">
            <BookOpen className="h-4 w-4 mt-0.5 text-muted-foreground flex-shrink-0" />
            <h3 className="text-sm font-semibold leading-snug">
              {topEvent.headline}
            </h3>
          </div>
        )}

        {/* Narrative body */}
        <p className="text-sm text-muted-foreground leading-relaxed">
          {buildNarrativeExplanation(data)}
        </p>

        {/* Caveat */}
        <p className="text-xs text-amber-400 border-t border-border pt-3">
          This narrative is a model-generated interpretation, not a forecast.
          It reflects the system&rsquo;s current read of dominant forces and may
          shift as new data arrives.
        </p>
      </CardContent>
    </Card>
  );
}
