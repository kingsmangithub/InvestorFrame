import { SectionWrapper } from "./shared/section-wrapper";
import { SectionHeading } from "./shared/section-heading";
import { CtaButtons } from "./shared/cta-buttons";

export function FinalCtaSection() {
  return (
    <SectionWrapper id="final-cta" className="relative overflow-hidden">
      {/* Subtle radial glow behind the text */}
      <div
        aria-hidden
        className="pointer-events-none absolute inset-0 flex items-center justify-center"
      >
        <div className="h-[420px] w-[420px] rounded-full bg-[#3ECF8E]/[0.06] blur-[100px]" />
      </div>

      <div className="relative text-center">
        <SectionHeading
          title="Build a clearer frame for the market"
          subtitle="Explore the demo, review the code, or start building your own event-driven market workflow with InvestorFrame."
          centered
        />

        <CtaButtons size="lg" className="mt-10 justify-center" />
      </div>
    </SectionWrapper>
  );
}
