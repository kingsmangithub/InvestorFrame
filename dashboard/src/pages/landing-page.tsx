import { HeroSection } from "@/components/landing/hero-section";
import { WhatItDoesSection } from "@/components/landing/what-it-does-section";
import { HowItWorksSection } from "@/components/landing/how-it-works-section";
import { ProductSurfacesSection } from "@/components/landing/product-surfaces-section";
import { ScenarioShowcaseSection } from "@/components/landing/scenario-showcase-section";
import { ExampleOutputsSection } from "@/components/landing/example-outputs-section";
import { WhyDifferentSection } from "@/components/landing/why-different-section";
import { BuiltForSection } from "@/components/landing/built-for-section";
import { FaqSection } from "@/components/landing/faq-section";
import { FinalCtaSection } from "@/components/landing/final-cta-section";
import { LandingFooter } from "@/components/landing/landing-footer";

export function LandingPage() {
  return (
    <div className="min-h-screen bg-background text-foreground">
      {/* Landing nav */}
      <header className="sticky top-0 z-50 border-b border-[#24314F] bg-[#0B1020]/80 backdrop-blur-md">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
          <a href="#" className="text-lg font-bold tracking-tight">
            InvestorFrame
          </a>
          <nav className="hidden items-center gap-6 text-sm text-muted-foreground md:flex">
            <a href="#what" className="hover:text-foreground transition-colors">Product</a>
            <a href="#how" className="hover:text-foreground transition-colors">How It Works</a>
            <a href="#scenarios" className="hover:text-foreground transition-colors">Scenarios</a>
            <a href="#faq" className="hover:text-foreground transition-colors">FAQ</a>
          </nav>
          <div className="flex items-center gap-3">
            <a
              href="#"
              className="hidden text-sm text-muted-foreground hover:text-foreground transition-colors sm:block"
            >
              GitHub
            </a>
            <a
              href="/dashboard"
              className="inline-flex h-8 items-center rounded-md bg-[#3ECF8E] px-4 text-sm font-medium text-[#0B1020] hover:bg-[#3ECF8E]/90 transition-colors"
            >
              Explore Demo
            </a>
          </div>
        </div>
      </header>

      <main>
        <HeroSection />
        <div id="what"><WhatItDoesSection /></div>
        <div id="how"><HowItWorksSection /></div>
        <ProductSurfacesSection />
        <div id="scenarios"><ScenarioShowcaseSection /></div>
        <ExampleOutputsSection />
        <WhyDifferentSection />
        <BuiltForSection />
        <div id="faq"><FaqSection /></div>
        <FinalCtaSection />
      </main>

      <LandingFooter />
    </div>
  );
}
