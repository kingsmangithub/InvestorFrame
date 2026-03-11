import { useState } from "react";
import { PageHeader } from "@/components/shared/page-header";
import { LoadingSkeleton } from "@/components/shared/loading-skeleton";
import { ErrorState } from "@/components/shared/error-state";
import { ScenarioControlPanel } from "@/components/scenario/scenario-control-panel";
import { ScenarioSummaryCard } from "@/components/scenario/scenario-summary-card";
import { ScenarioMarketImpact } from "@/components/scenario/scenario-market-impact";
import { ScenarioSectorImpact } from "@/components/scenario/scenario-sector-impact";
import { ScenarioWatchlistImpact } from "@/components/scenario/scenario-watchlist-impact";
import { ScenarioReportPanel } from "@/components/scenario/scenario-report-panel";
import { useScenario } from "@/lib/api/queries";
import { Card, CardContent } from "@/components/ui/card";
import { Beaker } from "lucide-react";

export function ScenarioLabPage() {
  const [selectedScenario, setSelectedScenario] = useState("");
  const scenario = useScenario();

  const handleRun = () => {
    if (!selectedScenario) return;
    scenario.mutate({ scenario_name: selectedScenario });
  };

  const handleReset = () => {
    setSelectedScenario("");
    scenario.reset();
  };

  return (
    <div className="space-y-6">
      <PageHeader
        title="Scenario Lab"
        subtitle="Change the world, then observe the market frame."
      />

      {/* Controls + Summary — side by side */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-4">
        <div className="lg:col-span-5">
          <ScenarioControlPanel
            selectedScenario={selectedScenario}
            onSelect={setSelectedScenario}
            onRun={handleRun}
            onReset={handleReset}
            isRunning={scenario.isPending}
          />
        </div>
        <div className="lg:col-span-7">
          {scenario.isPending ? (
            <LoadingSkeleton variant="card" />
          ) : scenario.isError ? (
            <ErrorState
              title="Scenario simulation failed."
              message="Please review your inputs and try again."
              onRetry={handleRun}
            />
          ) : scenario.data ? (
            <ScenarioSummaryCard data={scenario.data} />
          ) : (
            <ScenarioPlaceholder />
          )}
        </div>
      </div>

      {/* Results — only show when we have data */}
      {scenario.data && (
        <>
          {/* Market Impact + Sector Impact — side by side */}
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-4">
            <div className="lg:col-span-5">
              <ScenarioMarketImpact data={scenario.data} />
            </div>
            <div className="lg:col-span-7">
              <ScenarioSectorImpact data={scenario.data} />
            </div>
          </div>

          {/* Watchlist Impact — full width */}
          <ScenarioWatchlistImpact data={scenario.data} />

          {/* Report — full width */}
          <ScenarioReportPanel data={scenario.data} />
        </>
      )}
    </div>
  );
}

function ScenarioPlaceholder() {
  return (
    <Card className="h-full">
      <CardContent className="flex flex-col items-center justify-center h-full min-h-[280px] text-center">
        <Beaker className="h-10 w-10 text-muted-foreground mb-4" />
        <h3 className="text-sm font-semibold">No scenario has been run yet.</h3>
        <p className="text-xs text-muted-foreground mt-1 max-w-xs">
          Select an event and click &ldquo;Run Scenario&rdquo; to generate a simulation.
        </p>
      </CardContent>
    </Card>
  );
}
