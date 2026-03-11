import { TrendingUp, TrendingDown } from "lucide-react";
import { SectionWrapper } from "./shared/section-wrapper";
import { SectionHeading } from "./shared/section-heading";
import { cn } from "@/lib/utils";

const scenarios = [
  {
    title: "Hot CPI",
    description: "See how inflation pressure may shift the regime, weaken duration-sensitive growth, and reshape sector leadership.",
    direction: "negative" as const,
    color: {
      dot: "bg-red-500",
      text: "text-red-400",
      border: "border-red-500/20",
      bg: "bg-red-500/10",
    },
  },
  {
    title: "Dovish Fed",
    description: "Explore how softer policy expectations can change risk appetite and support rate-sensitive sectors.",
    direction: "positive" as const,
    color: {
      dot: "bg-emerald-500",
      text: "text-emerald-400",
      border: "border-emerald-500/20",
      bg: "bg-emerald-500/10",
    },
  },
  {
    title: "War Escalation",
    description: "Model how geopolitical stress may reprice energy, defensives, and risk appetite.",
    direction: "negative" as const,
    color: {
      dot: "bg-amber-500",
      text: "text-amber-400",
      border: "border-amber-500/20",
      bg: "bg-amber-500/10",
    },
  },
  {
    title: "Stronger AI Capex",
    description: "Test how a renewed AI investment cycle may reinforce tech leadership — or increase crowding risk.",
    direction: "positive" as const,
    color: {
      dot: "bg-indigo-500",
      text: "text-indigo-400",
      border: "border-indigo-500/20",
      bg: "bg-indigo-500/10",
    },
  },
] as const;

export function ScenarioShowcaseSection() {
  return (
    <SectionWrapper id="scenario-showcase">
      <SectionHeading
        title="What if the world changes from here?"
        subtitle="InvestorFrame is not just a dashboard. It is a market sandbox."
        centered
      />

      <div className="grid sm:grid-cols-2 gap-5 mt-12">
        {scenarios.map((scenario) => (
          <div
            key={scenario.title}
            className={cn(
              "rounded-xl border border-[#24314F] bg-[#151E32] p-5",
              "hover:border-[#3ECF8E]/20 transition-colors",
            )}
          >
            <div className="flex items-start justify-between gap-3">
              <div>
                <h3 className="font-semibold text-foreground">
                  {scenario.title}
                </h3>
                <p className="text-sm text-muted-foreground mt-1">
                  {scenario.description}
                </p>
              </div>

              <div
                className={cn(
                  "shrink-0 flex items-center gap-1.5 rounded-full px-2.5 py-1 text-xs font-medium",
                  scenario.color.bg,
                  scenario.color.text,
                  "border",
                  scenario.color.border,
                )}
              >
                {scenario.direction === "positive" ? (
                  <TrendingUp className="h-3 w-3" />
                ) : (
                  <TrendingDown className="h-3 w-3" />
                )}
                {scenario.direction === "positive" ? "Bullish" : "Bearish"}
              </div>
            </div>
          </div>
        ))}
      </div>
    </SectionWrapper>
  );
}
