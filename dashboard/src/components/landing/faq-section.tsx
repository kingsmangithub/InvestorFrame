import { useState } from "react";
import { ChevronDown } from "lucide-react";
import { cn } from "@/lib/utils";
import { SectionWrapper } from "./shared/section-wrapper";
import { SectionHeading } from "./shared/section-heading";

const faqs = [
  {
    question: "Is InvestorFrame a trading system?",
    answer:
      "No. InvestorFrame is a research and decision-support product. It helps interpret market structure, not automate trading.",
  },
  {
    question: "Does it provide buy or sell recommendations?",
    answer:
      "Not as deterministic signals. InvestorFrame provides regime framing, sector transmission, watchlist alignment, and scenario-based interpretation.",
  },
  {
    question: "What makes it different from a stock screener?",
    answer:
      "A stock screener starts with stocks. InvestorFrame starts with the market environment and traces how that environment affects sectors and watchlists.",
  },
  {
    question: "Can I test hypothetical scenarios?",
    answer:
      "Yes. Scenario Lab is designed to stress-test how changes in macro, policy, or geopolitical inputs may shift the current market frame.",
  },
  {
    question: "Is it only for equities?",
    answer:
      "The first version focuses on equities and global macro context, but the framing engine is designed to handle cross-asset signals as well.",
  },
] as const;

function FaqItem({
  question,
  answer,
}: {
  question: string;
  answer: string;
}) {
  const [open, setOpen] = useState(false);

  return (
    <div className="border-b border-[#24314F]">
      <button
        type="button"
        onClick={() => setOpen((prev) => !prev)}
        className="flex w-full items-center justify-between gap-4 py-5 text-left"
      >
        <span className="font-medium">{question}</span>
        <ChevronDown
          className={cn(
            "h-5 w-5 shrink-0 text-muted-foreground transition-transform duration-200",
            open && "rotate-180",
          )}
        />
      </button>

      <div
        className={cn(
          "grid transition-[grid-template-rows] duration-200",
          open ? "grid-rows-[1fr]" : "grid-rows-[0fr]",
        )}
      >
        <div className="overflow-hidden">
          <p className="pb-5 text-sm text-muted-foreground">{answer}</p>
        </div>
      </div>
    </div>
  );
}

export function FaqSection() {
  return (
    <SectionWrapper id="faq">
      <SectionHeading title="Frequently asked questions" centered />

      <div className="mx-auto mt-12 max-w-3xl">
        {faqs.map((faq) => (
          <FaqItem
            key={faq.question}
            question={faq.question}
            answer={faq.answer}
          />
        ))}
      </div>
    </SectionWrapper>
  );
}
