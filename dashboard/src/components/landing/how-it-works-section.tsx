import { SectionWrapper } from "./shared/section-wrapper";
import { SectionHeading } from "./shared/section-heading";
import { cn } from "@/lib/utils";

const steps = [
  {
    number: 1,
    title: "Event Ingestion",
    description:
      "Capture the market-moving signals that matter: macro releases, policy tone, geopolitical shocks, and narrative shifts.",
  },
  {
    number: 2,
    title: "Regime Framing",
    description:
      "Translate those signals into a coherent market frame with confidence, contradictions, and uncertainty.",
  },
  {
    number: 3,
    title: "Sector Transmission",
    description:
      "Identify which sectors are supported, pressured, or caught in mixed crosscurrents.",
  },
  {
    number: 4,
    title: "Watchlist Mapping",
    description:
      "Evaluate how your core names fit the current market frame.",
  },
  {
    number: 5,
    title: "Scenario Simulation",
    description:
      "Change one variable, then observe how the frame, sectors, and watchlist may respond.",
  },
] as const;

export function HowItWorksSection() {
  return (
    <SectionWrapper id="how-it-works">
      <SectionHeading
        title="How InvestorFrame works"
        subtitle="From event ingestion to regime framing — five steps to a complete market view."
        centered
      />

      {/* Desktop: horizontal flow */}
      <div className="hidden md:grid md:grid-cols-5 gap-4 mt-14">
        {steps.map((step, idx) => (
          <div key={step.number} className="relative flex flex-col items-center text-center">
            {/* Connecting line */}
            {idx < steps.length - 1 && (
              <div
                className="absolute top-4 left-[calc(50%+20px)] w-[calc(100%-40px)] border-t border-dashed border-[#24314F]"
                aria-hidden
              />
            )}

            <div
              className={cn(
                "relative z-10 w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold",
                "bg-[#3ECF8E]/10 text-[#3ECF8E] border border-[#3ECF8E]/20",
              )}
            >
              {step.number}
            </div>

            <h3 className="text-sm font-semibold text-foreground mt-4">
              {step.title}
            </h3>
            <p className="text-xs text-muted-foreground mt-1.5 leading-relaxed">
              {step.description}
            </p>
          </div>
        ))}
      </div>

      {/* Mobile: vertical flow */}
      <div className="md:hidden mt-10 space-y-0">
        {steps.map((step, idx) => (
          <div key={step.number} className="relative flex gap-4">
            {/* Vertical line + circle */}
            <div className="flex flex-col items-center">
              <div
                className={cn(
                  "w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold shrink-0",
                  "bg-[#3ECF8E]/10 text-[#3ECF8E] border border-[#3ECF8E]/20",
                )}
              >
                {step.number}
              </div>
              {idx < steps.length - 1 && (
                <div className="w-px flex-1 border-l border-dashed border-[#24314F] my-1" />
              )}
            </div>

            {/* Content */}
            <div className="pb-8">
              <h3 className="text-sm font-semibold text-foreground">
                {step.title}
              </h3>
              <p className="text-xs text-muted-foreground mt-1 leading-relaxed">
                {step.description}
              </p>
            </div>
          </div>
        ))}
      </div>
    </SectionWrapper>
  );
}
