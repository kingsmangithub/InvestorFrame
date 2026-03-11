import { CheckCircle2 } from "lucide-react";
import { SectionWrapper } from "./shared/section-wrapper";
import { SectionHeading } from "./shared/section-heading";

const points = [
  {
    title: "Event-first, not ticker-first",
    description:
      "InvestorFrame starts with the forces shaping the market — not just price action.",
  },
  {
    title: "Regime-aware, not context-blind",
    description:
      "The same event can mean different things under different market regimes.",
  },
  {
    title: "Explainable, not black-box",
    description:
      "Every output includes drivers, confidence, risk flags, and uncertainty.",
  },
  {
    title: "Scenario-based, not static",
    description:
      "Use the system to test changes in the world, not just describe the present.",
  },
] as const;

export function WhyDifferentSection() {
  return (
    <SectionWrapper id="why-different">
      <SectionHeading title="Not another ticker-first stock tool" centered />

      <div className="mt-12 grid grid-cols-1 sm:grid-cols-2 gap-6">
        {points.map((point) => (
          <div
            key={point.title}
            className="flex items-start gap-4 rounded-2xl border border-[#24314F] bg-card p-6"
          >
            <CheckCircle2 className="mt-0.5 h-5 w-5 shrink-0 text-[#3ECF8E]" />
            <div>
              <p className="font-semibold">{point.title}</p>
              <p className="mt-1 text-sm text-muted-foreground">
                {point.description}
              </p>
            </div>
          </div>
        ))}
      </div>
    </SectionWrapper>
  );
}
