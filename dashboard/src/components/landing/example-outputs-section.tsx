import { SectionWrapper } from "./shared/section-wrapper";
import { SectionHeading } from "./shared/section-heading";
import { cn } from "@/lib/utils";

/* ---------- mock data ---------- */

const sectorRows = [
  { ticker: "XLK", label: "Technology", score: 72.4, positive: true },
  { ticker: "XLF", label: "Financials", score: 22.7, positive: true },
  { ticker: "XLE", label: "Energy", score: -12.4, positive: false },
  { ticker: "XLU", label: "Utilities", score: -28.3, positive: false },
];

const watchlistRows = [
  {
    ticker: "NVDA",
    label: "Strong Tailwind",
    score: 66.8,
    positive: true,
    color: "text-emerald-400",
    badgeBg: "bg-emerald-500/15",
    badgeBorder: "border-emerald-500/25",
  },
  {
    ticker: "JPM",
    label: "Mixed",
    score: 12.4,
    positive: true,
    color: "text-amber-400",
    badgeBg: "bg-amber-500/15",
    badgeBorder: "border-amber-500/25",
  },
  {
    ticker: "XOM",
    label: "Headwind",
    score: -13.2,
    positive: false,
    color: "text-red-400",
    badgeBg: "bg-red-500/15",
    badgeBorder: "border-red-500/25",
  },
];

const drivers = [
  { label: "Strong jobs data", impact: "+8.2" },
  { label: "Fed rhetoric hawkish", impact: "-3.1" },
  { label: "AI capex guidance", impact: "+11.6" },
];

/* ---------- sub-components ---------- */

function CardShell({
  title,
  children,
}: {
  title: string;
  children: React.ReactNode;
}) {
  return (
    <div
      className={cn(
        "rounded-2xl border border-[#24314F] bg-[#151E32] overflow-hidden",
        "shadow-lg shadow-black/10",
      )}
    >
      <div className="px-5 pt-4 pb-3 border-b border-[#24314F]">
        <span className="text-xs font-medium uppercase tracking-wider text-muted-foreground">
          {title}
        </span>
      </div>
      <div className="p-5">{children}</div>
    </div>
  );
}

function MarketFrameCard() {
  return (
    <CardShell title="Market Frame">
      {/* Regime row */}
      <div className="flex items-center gap-3 mb-5">
        <span
          className={cn(
            "inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-semibold",
            "bg-emerald-500/15 text-emerald-400 border border-emerald-500/25",
          )}
        >
          Risk-On
        </span>
        <span className="text-2xl font-bold tracking-tight text-foreground">
          64.8
        </span>
        <span className="text-xs text-muted-foreground">Confidence 69%</span>
      </div>

      {/* Key drivers */}
      <p className="text-xs font-medium text-muted-foreground uppercase tracking-wider mb-2">
        Key Drivers
      </p>
      <div className="space-y-1.5">
        {drivers.map((d) => (
          <div
            key={d.label}
            className="flex items-center justify-between text-xs"
          >
            <span className="text-foreground/80">{d.label}</span>
            <span
              className={cn(
                "font-mono",
                d.impact.startsWith("+")
                  ? "text-emerald-400"
                  : "text-red-400",
              )}
            >
              {d.impact}
            </span>
          </div>
        ))}
      </div>
    </CardShell>
  );
}

function SectorViewCard() {
  return (
    <CardShell title="Sector View">
      <div className="space-y-3">
        {sectorRows.map((row) => (
          <div key={row.ticker} className="flex items-center gap-3">
            <span className="w-8 text-xs font-mono text-muted-foreground">
              {row.ticker}
            </span>
            <div className="flex-1 h-2 rounded-full bg-[#0B1020]">
              <div
                className={cn(
                  "h-full rounded-full",
                  row.positive ? "bg-emerald-500" : "bg-red-500",
                )}
                style={{
                  width: `${Math.min(Math.abs(row.score), 100)}%`,
                }}
              />
            </div>
            <span
              className={cn(
                "w-14 text-right text-xs font-mono",
                row.positive ? "text-emerald-400" : "text-red-400",
              )}
            >
              {row.positive ? "+" : ""}
              {row.score}
            </span>
          </div>
        ))}
      </div>
    </CardShell>
  );
}

function WatchlistImpactCard() {
  return (
    <CardShell title="Watchlist Impact">
      <div className="space-y-3">
        {watchlistRows.map((row) => (
          <div
            key={row.ticker}
            className="flex items-center justify-between gap-3"
          >
            <div className="flex items-center gap-3 min-w-0">
              <span className="text-sm font-mono font-semibold text-foreground">
                {row.ticker}
              </span>
              <span
                className={cn(
                  "inline-flex items-center rounded-full px-2 py-0.5 text-[10px] font-medium border",
                  row.badgeBg,
                  row.badgeBorder,
                  row.color,
                )}
              >
                {row.label}
              </span>
            </div>
            <span
              className={cn(
                "text-xs font-mono shrink-0",
                row.positive ? "text-emerald-400" : "text-red-400",
              )}
            >
              {row.positive ? "+" : ""}
              {row.score}
            </span>
          </div>
        ))}
      </div>
    </CardShell>
  );
}

/* ---------- main section ---------- */

export function ExampleOutputsSection() {
  return (
    <SectionWrapper id="example-outputs">
      <SectionHeading
        title="Outputs built for real interpretation"
        subtitle="Every result is structured, explainable, and uncertainty-aware."
        centered
      />

      <div className="grid md:grid-cols-3 gap-6 mt-12">
        <MarketFrameCard />
        <SectorViewCard />
        <WatchlistImpactCard />
      </div>
    </SectionWrapper>
  );
}
