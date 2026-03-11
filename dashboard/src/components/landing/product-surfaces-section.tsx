import { LayoutDashboard, FlaskConical, FileText } from "lucide-react";
import { SectionWrapper } from "./shared/section-wrapper";
import { SectionHeading } from "./shared/section-heading";
import { cn } from "@/lib/utils";

const surfaces = [
  {
    icon: LayoutDashboard,
    title: "Dashboard",
    description:
      "Get a clear view of today's market frame: dominant narrative, regime, sector leadership, and watchlist alignment.",
  },
  {
    icon: FlaskConical,
    title: "Scenario Lab",
    description:
      "Stress-test the market by changing one variable at a time — hot CPI, dovish Fed, war escalation, stronger AI capex, and more.",
  },
  {
    icon: FileText,
    title: "Reports & Explain",
    description:
      "Generate structured briefs and ask why the system sees the market the way it does.",
  },
] as const;

export function ProductSurfacesSection() {
  return (
    <SectionWrapper id="product-surfaces">
      <SectionHeading title="Three surfaces, one market frame" centered />

      <div className="grid md:grid-cols-3 gap-6 mt-12">
        {surfaces.map(({ icon: Icon, title, description }) => (
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
