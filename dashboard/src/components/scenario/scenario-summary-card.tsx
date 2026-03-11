import { ArrowRight } from "lucide-react";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { RegimeBadge } from "@/components/shared/regime-badge";
import type { ScenarioData } from "@/lib/api/types";

interface ScenarioSummaryCardProps {
  data: ScenarioData;
}

export function ScenarioSummaryCard({ data }: ScenarioSummaryCardProps) {
  const impact = data.regime_impact ?? {};
  const baselineRegime = (impact.baseline_state as string) ?? (impact.baseline_regime as string) ?? "unknown";
  const simulatedRegime = (impact.scenario_state as string) ?? (impact.simulated_regime as string) ?? "unknown";
  const shiftMagnitude = impact.shift_magnitude as string | undefined;
  const confidenceDelta = impact.confidence_delta as number | undefined;

  return (
    <Card>
      <CardHeader>
        <CardTitle>Scenario Summary</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        {/* Scenario identity */}
        <div>
          <p className="text-sm font-medium text-foreground">
            {data.scenario_name
              ?.replace(/_/g, " ")
              .replace(/\b\w/g, (c) => c.toUpperCase()) ?? "Unnamed Scenario"}
          </p>
          <p className="mt-0.5 text-xs text-muted-foreground">
            {data.description}
          </p>
        </div>

        {/* Regime transition */}
        <div className="flex items-center gap-3">
          <div className="space-y-1">
            <span className="text-xs text-muted-foreground">Current</span>
            <div>
              <RegimeBadge regime={baselineRegime} size="md" />
            </div>
          </div>
          <ArrowRight className="h-4 w-4 text-muted-foreground shrink-0 mt-4" />
          <div className="space-y-1">
            <span className="text-xs text-muted-foreground">Simulated</span>
            <div>
              <RegimeBadge regime={simulatedRegime} size="md" />
            </div>
          </div>
        </div>

        {/* Shift magnitude */}
        {shiftMagnitude && (
          <div className="rounded-md bg-muted/50 px-3 py-2">
            <span className="text-xs text-muted-foreground">Shift Magnitude</span>
            <p className="text-sm font-medium text-foreground capitalize">
              {shiftMagnitude.replace(/_/g, " ")}
            </p>
          </div>
        )}

        {/* Confidence delta */}
        {confidenceDelta != null && (
          <div className="rounded-md bg-muted/50 px-3 py-2">
            <span className="text-xs text-muted-foreground">Confidence Delta</span>
            <p className="text-sm font-medium tabular-nums text-foreground">
              {confidenceDelta > 0 ? "+" : ""}
              {(confidenceDelta * 100).toFixed(0)}%
            </p>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
