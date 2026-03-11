// Regime display config — colors match visual spec
export const REGIME_CONFIG = {
  risk_on: { label: "Risk-On", color: "bg-[#3ECF8E]/12 text-[#3ECF8E] border-[#3ECF8E]/25" },
  risk_off: { label: "Risk-Off", color: "bg-[#F05A7E]/12 text-[#F05A7E] border-[#F05A7E]/25" },
  uncertainty: { label: "Uncertainty", color: "bg-[#F59E0B]/12 text-[#F59E0B] border-[#F59E0B]/25" },
  transition: { label: "Transition", color: "bg-[#8D99AE]/12 text-[#8D99AE] border-[#8D99AE]/25" },
  neutral: { label: "Neutral", color: "bg-[#8D99AE]/12 text-[#8D99AE] border-[#8D99AE]/25" },
  inflation_scare: { label: "Inflation Scare", color: "bg-[#F59E0B]/14 text-[#F59E0B] border-[#F59E0B]/25" },
  growth_scare: { label: "Growth Scare", color: "bg-[#7C8CFF]/14 text-[#7C8CFF] border-[#7C8CFF]/25" },
} as const;

// Signal label display config
export const SIGNAL_CONFIG = {
  strong_tailwind: { label: "Strong Tailwind", color: "bg-[#3ECF8E]/12 text-[#3ECF8E]" },
  tailwind: { label: "Tailwind", color: "bg-[#1FA971]/12 text-[#3ECF8E]" },
  neutral: { label: "Neutral", color: "bg-[#8D99AE]/12 text-[#8D99AE]" },
  mixed: { label: "Mixed", color: "bg-[#F59E0B]/12 text-[#F59E0B]" },
  headwind: { label: "Headwind", color: "bg-[#F05A7E]/12 text-[#F05A7E]" },
  strong_headwind: { label: "Strong Headwind", color: "bg-[#D94368]/12 text-[#F05A7E]" },
} as const;

// Direction display config
export const DIRECTION_CONFIG = {
  bullish: { label: "Bullish", color: "text-[#3ECF8E]", arrow: "↑" },
  bearish: { label: "Bearish", color: "text-[#F05A7E]", arrow: "↓" },
  neutral: { label: "Neutral", color: "text-[#8D99AE]", arrow: "→" },
  mixed: { label: "Mixed", color: "text-[#F59E0B]", arrow: "↔" },
} as const;

// Sentiment label display config
export const SENTIMENT_CONFIG = {
  very_bullish: { label: "Very Bullish", color: "text-[#3ECF8E]" },
  bullish: { label: "Bullish", color: "text-[#3ECF8E]" },
  neutral: { label: "Neutral", color: "text-[#8D99AE]" },
  bearish: { label: "Bearish", color: "text-[#F05A7E]" },
  very_bearish: { label: "Very Bearish", color: "text-[#F05A7E]" },
} as const;

// Chart colors for Recharts — hex values matching signal system
export const CHART_COLORS = {
  positive: "#3ECF8E",
  negative: "#F05A7E",
  neutral: "#8D99AE",
  warning: "#F59E0B",
  special: "#7C8CFF",
  grid: "#24314F",
  text: "#7F8BA7",
  tooltipBg: "#151E32",
  tooltipBorder: "#24314F",
} as const;

// Scenario templates matching backend config/scenarios.yaml
export const SCENARIO_TEMPLATES = [
  { name: "fed_rate_hike_50bps", label: "Fed Rate Hike (+50bps)", description: "Federal Reserve raises rates by 50 basis points", category: "Macro" },
  { name: "fed_rate_cut_25bps", label: "Fed Rate Cut (-25bps)", description: "Federal Reserve cuts rates by 25 basis points", category: "Macro" },
  { name: "oil_price_shock", label: "Oil Price Shock", description: "Oil prices spike 20%+ due to supply disruption", category: "Commodity" },
  { name: "tech_earnings_miss", label: "Tech Earnings Miss", description: "Major tech companies miss earnings expectations", category: "Earnings" },
  { name: "geopolitical_escalation", label: "Geopolitical Escalation", description: "Major geopolitical conflict escalation", category: "Geopolitical" },
  { name: "tariff_war_escalation", label: "Tariff War Escalation", description: "Broad tariff increases on major trading partners", category: "Trade" },
  { name: "recession_signal", label: "Recession Signal", description: "Multiple recession indicators triggered", category: "Macro" },
  { name: "ai_breakthrough", label: "AI Breakthrough", description: "Major AI advancement with broad economic implications", category: "Technology" },
] as const;

export const SCENARIO_CATEGORIES = ["All", "Macro", "Commodity", "Earnings", "Geopolitical", "Trade", "Technology"] as const;

// Tooltips
export const TOOLTIPS = {
  regime: "Regime is the system's summary of the current market environment, combining macro signals, narrative pressure, and cross-asset context.",
  sentimentScore: "Sentiment Score reflects the current balance of supportive versus adverse market forces. It is not a price target.",
  confidence: "Confidence estimates how coherent and stable the current frame is, based on signal alignment and model certainty.",
  dominantNarrative: "Dominant Narrative describes the main story the market appears to be pricing right now.",
  sectorScore: "Sector Score reflects how strongly the current market frame supports or pressures a sector over the selected horizon.",
  alignment: "Alignment shows whether a watchlist name is currently supported, pressured, or pulled in mixed directions by the market frame.",
  severity: "Severity controls the assumed strength of the simulated shock. Higher values imply a stronger regime and sector response.",
  uncertainty: "Uncertainty highlights the factors most likely to invalidate or reverse the current interpretation.",
  riskFlags: "Risk Flags surface conditions that may weaken, reverse, or complicate the current view.",
} as const;
