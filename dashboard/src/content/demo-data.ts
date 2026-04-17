export type FrameData = {
  date: string;
  frame: {
    label: string;
    confidence: number;
    dominant_pressure: string;
    caution: string;
    action_bias: string;
  };
  questions: string[];
};

export type IdeaData = {
  ticker: string;
  company: string;
  action: string;
  business_summary: string;
  bull_case: string[];
  bear_case: string[];
  assumptions: string[];
  invalidation: string[];
  buy_conditions: string[];
  sell_conditions: string[];
};

export type ReviewData = {
  date: string;
  ticker: string;
  result: string;
  thesis_quality: number;
  process_quality: number;
  emotional_discipline: number;
  lesson: string;
};

export const frameData: FrameData = {
  date: "2026-04-17",
  frame: {
    label: "mixed",
    confidence: 0.62,
    dominant_pressure:
      "Rates have eased, but crowding in AI leaders keeps upside and disappointment tightly linked.",
    caution:
      "Do not let strong recent price action masquerade as proof of a durable thesis.",
    action_bias: "Selective. Waiting is better than forcing a trade.",
  },
  questions: [
    "What changed materially?",
    "What is still unclear?",
    "What deserves patience today?",
  ],
};

export const ideas: IdeaData[] = [
  {
    ticker: "MSFT",
    company: "Microsoft",
    action: "wait",
    business_summary:
      "A durable software and cloud platform with strong switching costs, resilient demand, and disciplined capital allocation.",
    bull_case: [
      "Cloud and productivity remain deeply embedded in enterprise workflows.",
      "AI may strengthen distribution across the existing ecosystem.",
      "Balance sheet quality lowers fragility.",
    ],
    bear_case: [
      "AI optimism may already be heavily priced in.",
      "Cloud growth could normalize faster than investors expect.",
      "Large-cap expectations reduce room for upside surprise.",
    ],
    assumptions: [
      "Enterprise demand remains sticky.",
      "AI monetization improves economics rather than just capex intensity.",
    ],
    invalidation: [
      "Cloud economics weaken materially.",
      "AI spending rises without durable monetization.",
    ],
    buy_conditions: [
      "Expected return improves relative to quality.",
      "The thesis survives a cooling-off period.",
    ],
    sell_conditions: [
      "Thesis quality weakens materially.",
      "A clearly better idea appears with a wider quality-to-price gap.",
    ],
  },
  {
    ticker: "COST",
    company: "Costco",
    action: "pass",
    business_summary:
      "A high-quality retailer with strong customer trust and membership economics, but often priced for near-perfection.",
    bull_case: [
      "Membership economics remain unusually durable.",
      "Operational consistency is a meaningful edge.",
    ],
    bear_case: [
      "Valuation can leave little room for disappointment.",
      "A great business is not automatically a great entry point.",
    ],
    assumptions: ["Membership renewal strength persists."],
    invalidation: ["Value perception weakens or unit economics deteriorate."],
    buy_conditions: ["Price offers a clearer gap between quality and expectations."],
    sell_conditions: ["Expectations become extreme or thesis is impaired."],
  },
];

export const reviews: ReviewData[] = [
  {
    date: "2026-04-10",
    ticker: "NVDA",
    result: "too_early_exit",
    thesis_quality: 7,
    process_quality: 5,
    emotional_discipline: 3,
    lesson: "I sold because the gain felt emotionally fragile, not because the thesis deteriorated.",
  },
  {
    date: "2026-04-03",
    ticker: "TSLA",
    result: "fomo_entry",
    thesis_quality: 3,
    process_quality: 2,
    emotional_discipline: 2,
    lesson: "I reacted to price acceleration without a written thesis or exit plan.",
  },
];

export const rulebook = {
  principles: [
    "Stay inside your circle of competence.",
    "Write the thesis before committing capital.",
    "Always write the anti-thesis.",
    "Price is not the thesis.",
    "No action is a valid action.",
    "Protect survival before chasing upside.",
  ],
  behaviorGate: [
    "Thesis is written before action.",
    "Anti-thesis is written.",
    "This is not a FOMO-driven action.",
    "I can explain what would prove me wrong.",
    "The position fits my risk budget.",
    "I would still want this after a 48-hour delay.",
  ],
  sellRules: [
    "Sell or trim when the original thesis breaks.",
    "Exit when predefined risk is breached.",
    "Do not average down just to get back to even.",
    "Reallocate only when a materially better idea exists.",
  ],
  wisdom: {
    mistakePatterns: [
      "Buying excitement instead of evidence.",
      "Holding losers because I want to get back to even.",
      "Selling winners because gains feel emotionally fragile.",
    ],
    goodPatterns: [
      "Decision quality improves when the anti-thesis is explicit.",
      "A short delay reduces the number of low-quality actions.",
    ],
  },
};

export function getIdeaByTicker(ticker?: string): IdeaData | undefined {
  return ideas.find((idea) => idea.ticker.toLowerCase() === ticker?.toLowerCase());
}
