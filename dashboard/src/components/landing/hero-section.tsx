import { SectionWrapper } from "./shared/section-wrapper";
import { CtaButtons } from "./shared/cta-buttons";
import { BadgePill } from "./shared/badge-pill";
import { cn } from "@/lib/utils";

const capabilityTags = [
  "Event-Driven",
  "Regime-Aware",
  "Explainable",
  "Scenario-Based",
  "Research-First",
];

const mockSectors = [
  { label: "XLK", value: 72.4, color: "bg-emerald-500" },
  { label: "XLF", value: 22.7, color: "bg-emerald-500" },
  { label: "XLE", value: -12.4, color: "bg-red-500" },
  { label: "XLU", value: -28.3, color: "bg-red-500" },
];

export function HeroSection() {
  return (
    <SectionWrapper id="hero" className="pt-24 md:pt-32 pb-16 md:pb-20">
      <div className="grid lg:grid-cols-2 gap-12 lg:gap-16 items-center">
        {/* Left: copy */}
        <div className="space-y-6">
          <h1 className="text-3xl md:text-5xl font-bold tracking-tight text-foreground">
            Frame the market before you trade it.
          </h1>

          <p className="text-lg text-muted-foreground max-w-xl leading-relaxed">
            InvestorFrame turns macro signals, geopolitical shocks, policy
            changes, and market narratives into explainable market frames, sector
            transmission, and what-if simulations.
          </p>

          <CtaButtons size="lg" className="pt-2" />

          <div className="flex flex-wrap gap-2 pt-2">
            {capabilityTags.map((tag) => (
              <BadgePill key={tag}>{tag}</BadgePill>
            ))}
          </div>
        </div>

        {/* Right: mock dashboard preview */}
        <div className="relative">
          <div
            className={cn(
              "rounded-2xl border border-[#24314F] bg-[#151E32] p-6",
              "shadow-xl shadow-black/20",
            )}
          >
            {/* Header row */}
            <div className="flex items-center justify-between mb-5">
              <span className="text-xs font-medium uppercase tracking-wider text-muted-foreground">
                Market Frame
              </span>
              <span className="text-xs text-muted-foreground">
                Live &middot; Mar 11 2026
              </span>
            </div>

            {/* Regime row */}
            <div className="flex items-center gap-4 mb-6">
              <span
                className={cn(
                  "inline-flex items-center rounded-full px-3 py-1 text-xs font-semibold",
                  "bg-emerald-500/15 text-emerald-400 border border-emerald-500/25",
                )}
              >
                Risk-On
              </span>
              <span className="text-3xl font-bold tracking-tight text-foreground">
                64.8
              </span>
              <span className="text-sm text-muted-foreground">
                Confidence 69%
              </span>
            </div>

            {/* Sector bars */}
            <div className="space-y-3">
              {mockSectors.map((sector) => (
                <div key={sector.label} className="flex items-center gap-3">
                  <span className="w-8 text-xs font-mono text-muted-foreground">
                    {sector.label}
                  </span>
                  <div className="flex-1 h-2 rounded-full bg-[#0B1020]">
                    <div
                      className={cn("h-full rounded-full", sector.color)}
                      style={{
                        width: `${Math.min(Math.abs(sector.value), 100)}%`,
                      }}
                    />
                  </div>
                  <span
                    className={cn(
                      "w-12 text-right text-xs font-mono",
                      sector.value >= 0
                        ? "text-emerald-400"
                        : "text-red-400",
                    )}
                  >
                    {sector.value >= 0 ? "+" : ""}
                    {sector.value}
                  </span>
                </div>
              ))}
            </div>
          </div>

          {/* Subtle glow effect behind the card */}
          <div
            className="absolute -inset-px rounded-2xl bg-gradient-to-b from-[#3ECF8E]/5 to-transparent -z-10 blur-xl"
            aria-hidden
          />
        </div>
      </div>
    </SectionWrapper>
  );
}
