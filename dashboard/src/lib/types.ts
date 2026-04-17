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

export type BehaviorData = {
  checks: string[];
  default_action: string;
};

export type WisdomData = {
  mistake_patterns: string[];
  good_patterns: string[];
};

export type RulebookData = {
  principles: string[];
  behavior_gate: string[];
  sell_rules: string[];
  wisdom: WisdomData;
};
