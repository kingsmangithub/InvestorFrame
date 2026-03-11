import { Activity, Layers, GitBranch } from "lucide-react";
import { SectionWrapper } from "./shared/section-wrapper";
import { SectionHeading } from "./shared/section-heading";
import { cn } from "@/lib/utils";

const features = [
  {
    icon: Activity,
    title: "Track what changed",
    description:
      "Follow macro events, policy signals, geopolitical shifts, yields, commodities, and market narratives.",
  },
  {
    icon: Layers,
    title: "Frame the regime",
    description:
      "Turn noisy inputs into a structured market frame: risk-on, risk-off, inflation scare, growth scare, and more.",
  },
  {
    icon: GitBranch,
    title: "Trace the transmission",
    description:
      "See how the current frame flows into sectors, factors, and your watchlist — with drivers, risk flags, and uncertainty.",
  },
] as const;

export function WhatItDoesSection() {
  return (
    <SectionWrapper id="what-it-does">
      <SectionHeading
        title="A better way to read the market"
        subtitle="Most tools start with tickers. InvestorFrame starts with the world."
        centered
      />

      <div className="grid md:grid-cols-3 gap-6 mt-12">
        {features.map(({ icon: Icon, title, description }) => (
          <div
            key={title}
            className={cn(
              "rounded-2xl border border-[#24314F] bg-[#151E32] p-6",
              "hover:border-[#3ECF8E]/30 transition-colors",
            )}
          >
            <div
              className={cn(
                "h-10 w-10 rounded-lg flex items-center justify-center",
                "bg-[#3ECF8E]/10 mb-4",
              )}
            >
              <Icon className="h-5 w-5 text-[#3ECF8E]" />
            </div>
            <h3 className="text-lg font-semibold text-foreground">{title}</h3>
            <p className="text-sm text-muted-foreground mt-2 leading-relaxed">
              {description}
            </p>
          </div>
        ))}
      </div>
    </SectionWrapper>
  );
}
