"use client";

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  Cell,
  ResponsiveContainer,
} from "recharts";
import { TrendingUp, TrendingDown } from "lucide-react";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { cn } from "@/lib/utils";
import { formatDelta } from "@/lib/utils";
import type { ScenarioData, ScenarioSectorDelta } from "@/lib/api/types";

interface ScenarioSectorImpactProps {
  data: ScenarioData;
}

function ChartTooltip({
  active,
  payload,
}: {
  active?: boolean;
  payload?: Array<{ payload: ScenarioSectorDelta }>;
}) {
  if (!active || !payload?.[0]) return null;
  const item = payload[0].payload;
  return (
    <div className="rounded-md border bg-card px-3 py-2 text-xs shadow-md">
      <p className="font-medium text-foreground">{item.name}</p>
      <p className="text-muted-foreground">
        Baseline: {item.baseline_score.toFixed(1)} | Scenario:{" "}
        {item.scenario_score.toFixed(1)}
      </p>
      <p
        className={cn(
          "font-medium tabular-nums",
          item.delta > 0 ? "text-emerald-400" : "text-rose-400",
        )}
      >
        Delta: {formatDelta(item.delta)}
      </p>
    </div>
  );
}

export function ScenarioSectorImpact({ data }: ScenarioSectorImpactProps) {
  const sectors = data.sector_impacts ?? [];
  const sorted = [...sectors].sort((a, b) => b.delta - a.delta);
  const positive = sorted.filter((s) => s.delta > 0);
  const negative = sorted.filter((s) => s.delta < 0);

  if (sectors.length === 0) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Sector Impact</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-muted-foreground">
            No sector impact data available for this scenario.
          </p>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Sector Impact</CardTitle>
        <CardDescription>
          The sectors most likely to benefit or come under pressure if this
          scenario plays out.
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-5">
        {/* Horizontal bar chart */}
        <div className="h-64">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart
              data={sorted}
              layout="vertical"
              margin={{ top: 0, right: 12, bottom: 0, left: 4 }}
            >
              <XAxis
                type="number"
                tick={{ fill: "hsl(var(--muted-foreground))", fontSize: 11 }}
                axisLine={false}
                tickLine={false}
              />
              <YAxis
                type="category"
                dataKey="symbol"
                tick={{ fill: "hsl(var(--muted-foreground))", fontSize: 11 }}
                axisLine={false}
                tickLine={false}
                width={48}
              />
              <Tooltip
                content={<ChartTooltip />}
                cursor={{ fill: "hsl(var(--muted))", opacity: 0.3 }}
              />
              <Bar dataKey="delta" radius={[0, 3, 3, 0]} maxBarSize={20}>
                {sorted.map((entry) => (
                  <Cell
                    key={entry.symbol}
                    fill={
                      entry.delta >= 0
                        ? "hsl(142, 71%, 45%)"
                        : "hsl(349, 89%, 60%)"
                    }
                  />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Sector lists */}
        <div className="grid gap-4 sm:grid-cols-2">
          {positive.length > 0 && (
            <div className="space-y-2">
              <div className="flex items-center gap-1.5 text-xs font-medium text-emerald-400">
                <TrendingUp className="h-3.5 w-3.5" />
                Positive Sectors
              </div>
              <ul className="space-y-1">
                {positive.map((s) => (
                  <li
                    key={s.symbol}
                    className="flex items-center justify-between text-sm"
                  >
                    <span className="text-muted-foreground">{s.name}</span>
                    <span className="font-medium tabular-nums text-emerald-400">
                      {formatDelta(s.delta)}
                    </span>
                  </li>
                ))}
              </ul>
            </div>
          )}
          {negative.length > 0 && (
            <div className="space-y-2">
              <div className="flex items-center gap-1.5 text-xs font-medium text-rose-400">
                <TrendingDown className="h-3.5 w-3.5" />
                Negative Sectors
              </div>
              <ul className="space-y-1">
                {negative.map((s) => (
                  <li
                    key={s.symbol}
                    className="flex items-center justify-between text-sm"
                  >
                    <span className="text-muted-foreground">{s.name}</span>
                    <span className="font-medium tabular-nums text-rose-400">
                      {formatDelta(s.delta)}
                    </span>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
}
