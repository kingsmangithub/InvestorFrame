import { AlertTriangle } from "lucide-react";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import type { ScenarioData } from "@/lib/api/types";

interface ScenarioMarketImpactProps {
  data: ScenarioData;
}

function buildMarketSummary(data: ScenarioData): string {
  const impact = data.regime_impact ?? {};
  const baseline = (impact.baseline_regime as string) ?? "the current regime";
  const simulated = (impact.simulated_regime as string) ?? "the simulated regime";
  const magnitude = (impact.shift_magnitude as string) ?? "an unspecified degree";

  const positiveSectors = data.sector_impacts?.filter((s) => s.delta > 0).length ?? 0;
  const negativeSectors = data.sector_impacts?.filter((s) => s.delta < 0).length ?? 0;
  const totalStocks = data.watchlist_impacts?.length ?? 0;

  const regimeShift =
    baseline === simulated
      ? `The simulated event is not expected to alter the current regime classification.`
      : `This scenario projects a regime shift from ${baseline.replace(/_/g, " ")} to ${simulated.replace(/_/g, " ")}, with a ${magnitude} degree of displacement.`;

  const sectorLine =
    positiveSectors > 0 || negativeSectors > 0
      ? ` Across tracked sectors, ${positiveSectors} show improved conditions while ${negativeSectors} face increased pressure.`
      : "";

  const stockLine =
    totalStocks > 0
      ? ` The scenario also affects ${totalStocks} watchlist name${totalStocks !== 1 ? "s" : ""}, with varying degrees of signal displacement.`
      : "";

  return `${regimeShift}${sectorLine}${stockLine}`;
}

export function ScenarioMarketImpact({ data }: ScenarioMarketImpactProps) {
  const uncertainties = data.uncertainty_notes ?? [];

  return (
    <Card>
      <CardHeader>
        <CardTitle>Market Impact</CardTitle>
        <CardDescription>
          How the simulated event changes the broader market frame.
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        {/* Summary paragraph */}
        <p className="text-sm leading-relaxed text-muted-foreground">
          {buildMarketSummary(data)}
        </p>

        {/* Uncertainty notes */}
        {uncertainties.length > 0 && (
          <div className="space-y-2">
            <p className="text-xs font-medium text-muted-foreground uppercase tracking-wider">
              Uncertainty Factors
            </p>
            <ul className="space-y-1.5">
              {uncertainties.map((note, i) => (
                <li key={i} className="flex items-start gap-2 text-sm">
                  <AlertTriangle className="mt-0.5 h-3.5 w-3.5 shrink-0 text-amber-400" />
                  <span className="text-muted-foreground">{note}</span>
                </li>
              ))}
            </ul>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
