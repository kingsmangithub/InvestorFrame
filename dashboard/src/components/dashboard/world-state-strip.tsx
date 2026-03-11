import { MetricCard } from "@/components/shared/metric-card";
import type { MarketData } from "@/lib/api/types";
import { EmptyState } from "@/components/shared/empty-state";

interface WorldStateStripProps {
  data: MarketData;
}

const INDICATOR_LABELS: { key: string; label: string }[] = [
  { key: "fed_stance", label: "Fed Stance" },
  { key: "inflation_pressure", label: "Inflation Pressure" },
  { key: "growth_pressure", label: "Growth Pressure" },
  { key: "geo_risk", label: "Geo Risk" },
  { key: "ai_narrative_heat", label: "AI Narrative Heat" },
  { key: "yields_usd", label: "Yields / USD" },
];

function deriveLevel(value: number): string {
  if (value >= 0.75) return "Elevated";
  if (value >= 0.5) return "Moderate";
  if (value >= 0.25) return "Low";
  return "Subdued";
}

function deriveDetail(
  key: string,
  factors: string[],
): string | undefined {
  const keyword = key.replace(/_/g, " ").split(" ")[0] ?? key;
  const match = factors.find((f) =>
    f.toLowerCase().includes(keyword),
  );
  return match;
}

export function WorldStateStrip({ data }: WorldStateStripProps) {
  if (!data.regime) {
    return (
      <EmptyState
        title="World state unavailable"
        message="Regime data has not been computed for this period."
      />
    );
  }

  const indicators = data.regime.indicator_values;
  const factors = data.regime.contributing_factors;

  return (
    <section>
      <div className="mb-3">
        <h2 className="text-sm font-semibold tracking-wide">World State</h2>
        <p className="text-xs text-muted-foreground mt-0.5">
          A quick snapshot of the forces shaping today&rsquo;s market backdrop.
        </p>
      </div>
      <div className="flex gap-3 overflow-x-auto pb-2 scrollbar-thin">
        {INDICATOR_LABELS.map(({ key, label }) => {
          const raw = indicators[key];
          const value = raw != null ? deriveLevel(raw) : "N/A";
          const detail = deriveDetail(key, factors);

          return (
            <MetricCard
              key={key}
              label={label}
              value={value}
              detail={detail}
            />
          );
        })}
      </div>
    </section>
  );
}
