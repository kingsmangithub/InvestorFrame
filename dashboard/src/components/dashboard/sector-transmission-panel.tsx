import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { DirectionBadge } from "@/components/shared/direction-badge";
import { EmptyState } from "@/components/shared/empty-state";
import { formatConfidence } from "@/lib/utils";
import type { SectorsData } from "@/lib/api/types";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  ResponsiveContainer,
  Cell,
  Tooltip,
} from "recharts";

interface SectorTransmissionPanelProps {
  data: SectorsData;
}

export function SectorTransmissionPanel({ data }: SectorTransmissionPanelProps) {
  if (!data.sectors || data.sectors.length === 0) {
    return (
      <Card>
        <CardHeader>
          <CardTitle className="text-base">Sector Transmission</CardTitle>
        </CardHeader>
        <CardContent>
          <EmptyState
            title="No sector data"
            message="Sector scores have not been computed for the current period."
          />
        </CardContent>
      </Card>
    );
  }

  const sorted = [...data.sectors].sort((a, b) => b.score - a.score);
  const chartData = sorted.map((s) => ({
    name: s.symbol,
    score: s.score,
    fullName: s.name,
  }));

  const topSectors = sorted.filter((s) => s.score > 0);
  const pressuredSectors = sorted.filter((s) => s.score <= 0);

  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-base">Sector Transmission</CardTitle>
        <CardDescription>
          How the current market frame is flowing through sector leadership.
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-5">
        {/* Chart */}
        <div className="h-64">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={chartData} layout="vertical" margin={{ left: 4, right: 16 }}>
              <XAxis type="number" hide />
              <YAxis
                type="category"
                dataKey="name"
                width={50}
                tick={{ fill: "hsl(var(--muted-foreground))", fontSize: 11 }}
                axisLine={false}
                tickLine={false}
              />
              <Tooltip
                cursor={{ fill: "hsl(var(--muted) / 0.3)" }}
                contentStyle={{
                  backgroundColor: "hsl(var(--card))",
                  border: "1px solid hsl(var(--border))",
                  borderRadius: "6px",
                  fontSize: "12px",
                }}
                labelStyle={{ color: "hsl(var(--foreground))" }}
                formatter={(value: number) => [value.toFixed(2), "Score"]}
              />
              <Bar dataKey="score" radius={[0, 4, 4, 0]} maxBarSize={20}>
                {chartData.map((entry) => (
                  <Cell
                    key={entry.name}
                    fill={entry.score > 0 ? "hsl(142 71% 45%)" : "hsl(347 77% 50%)"}
                  />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Sector lists */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          {topSectors.length > 0 && (
            <div>
              <h4 className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-2">
                Top Sectors
              </h4>
              <ul className="space-y-1.5">
                {topSectors.map((s) => (
                  <li key={s.symbol} className="flex items-center justify-between text-sm">
                    <span className="truncate">{s.name}</span>
                    <div className="flex items-center gap-2 ml-2 flex-shrink-0">
                      <DirectionBadge direction={s.direction} />
                      <span className="text-xs text-muted-foreground tabular-nums">
                        {formatConfidence(s.confidence)}
                      </span>
                    </div>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {pressuredSectors.length > 0 && (
            <div>
              <h4 className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-2">
                Pressured Sectors
              </h4>
              <ul className="space-y-1.5">
                {pressuredSectors.map((s) => (
                  <li key={s.symbol} className="flex items-center justify-between text-sm">
                    <span className="truncate">{s.name}</span>
                    <div className="flex items-center gap-2 ml-2 flex-shrink-0">
                      <DirectionBadge direction={s.direction} />
                      <span className="text-xs text-muted-foreground tabular-nums">
                        {formatConfidence(s.confidence)}
                      </span>
                    </div>
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
