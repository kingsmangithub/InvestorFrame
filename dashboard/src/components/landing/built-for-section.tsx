import { BookOpen, PenTool, TrendingUp } from "lucide-react";
import { SectionWrapper } from "./shared/section-wrapper";
import { SectionHeading } from "./shared/section-heading";

const audiences = [
  {
    label: "Investors",
    icon: TrendingUp,
    description:
      "Understand the market frame before reacting to headlines.",
  },
  {
    label: "Researchers",
    icon: BookOpen,
    description:
      "Turn messy event flows into structured regime and sector logic.",
  },
  {
    label: "Writers & Analysts",
    icon: PenTool,
    description:
      "Use scenario-based explanations to communicate what the market may be pricing.",
  },
] as const;

export function BuiltForSection() {
  return (
    <SectionWrapper id="built-for">
      <SectionHeading
        title="Built for investors, researchers, and market storytellers"
        centered
      />

      <div className="mt-12 grid grid-cols-1 md:grid-cols-3 gap-6">
        {audiences.map((audience) => (
          <div
            key={audience.label}
            className="rounded-2xl border border-[#24314F] bg-card p-6"
          >
            <audience.icon className="h-6 w-6 text-[#3ECF8E]" />
            <h3 className="mt-4 text-lg font-semibold">{audience.label}</h3>
            <p className="mt-2 text-sm text-muted-foreground">
              {audience.description}
            </p>
          </div>
        ))}
      </div>
    </SectionWrapper>
  );
}
