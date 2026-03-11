import type { ScenarioData } from "@/lib/api/types";

export const mockScenarioResults: Record<string, ScenarioData> = {
  fed_rate_hike_50bps: {
    scenario_name: "fed_rate_hike_50bps",
    description: "Federal Reserve raises rates by 50 basis points",
    regime_impact: {
      baseline_state: "risk_on",
      scenario_state: "uncertainty",
      shift_magnitude: "strong_negative",
    },
    sector_impacts: [
      { symbol: "XLK", name: "Technology", baseline_score: 72.4, scenario_score: 28.1, delta: -44.3, direction_change: true },
      { symbol: "XLC", name: "Communication Services", baseline_score: 58.1, scenario_score: 22.4, delta: -35.7, direction_change: true },
      { symbol: "XLY", name: "Consumer Discretionary", baseline_score: 41.3, scenario_score: 5.2, delta: -36.1, direction_change: true },
      { symbol: "XLF", name: "Financials", baseline_score: 22.7, scenario_score: 45.8, delta: 23.1, direction_change: false },
      { symbol: "XLE", name: "Energy", baseline_score: -12.4, scenario_score: -8.1, delta: 4.3, direction_change: false },
      { symbol: "XLU", name: "Utilities", baseline_score: -28.3, scenario_score: -42.1, delta: -13.8, direction_change: false },
      { symbol: "XLP", name: "Consumer Staples", baseline_score: -18.9, scenario_score: 12.4, delta: 31.3, direction_change: true },
      { symbol: "XLV", name: "Healthcare", baseline_score: 8.6, scenario_score: 25.3, delta: 16.7, direction_change: false },
    ],
    watchlist_impacts: [
      { symbol: "NVDA", name: "NVIDIA", baseline_signal: 66.8, scenario_signal: 18.2, delta: -48.6, label_change: "strong_tailwind → mixed" },
      { symbol: "MSFT", name: "Microsoft", baseline_signal: 53.2, scenario_signal: 15.8, delta: -37.4, label_change: "tailwind → mixed" },
      { symbol: "AMZN", name: "Amazon", baseline_signal: 40.7, scenario_signal: -5.2, delta: -45.9, label_change: "tailwind → headwind" },
      { symbol: "JPM", name: "JPMorgan Chase", baseline_signal: 12.4, scenario_signal: 38.6, delta: 26.2, label_change: "mixed → tailwind" },
      { symbol: "XOM", name: "Exxon Mobil", baseline_signal: -13.2, scenario_signal: -8.4, delta: 4.8, label_change: null },
      { symbol: "AAPL", name: "Apple", baseline_signal: 25.9, scenario_signal: -2.1, delta: -28.0, label_change: "tailwind → mixed" },
      { symbol: "NEM", name: "Newmont", baseline_signal: -26.2, scenario_signal: -12.8, delta: 13.4, label_change: null },
      { symbol: "GOOGL", name: "Alphabet", baseline_signal: 47.8, scenario_signal: 12.3, delta: -35.5, label_change: "tailwind → mixed" },
    ],
    uncertainty_notes: [
      "Actual market reaction depends heavily on forward guidance language.",
      "Positioning may amplify the initial move before mean-reverting.",
      "A 50bps hike in the current context would be a significant surprise.",
    ],
  },
};

// Generate quick results for other scenarios with common structure
export function getMockScenarioResult(scenarioName: string): ScenarioData | null {
  if (mockScenarioResults[scenarioName]) {
    return mockScenarioResults[scenarioName];
  }

  // Default mock for any template
  return {
    scenario_name: scenarioName,
    description: `Simulated scenario: ${scenarioName.replace(/_/g, " ")}`,
    regime_impact: {
      baseline_state: "risk_on",
      scenario_state: "uncertainty",
      shift_magnitude: "moderate_negative",
    },
    sector_impacts: [
      { symbol: "XLK", name: "Technology", baseline_score: 72.4, scenario_score: 45.2, delta: -27.2, direction_change: false },
      { symbol: "XLF", name: "Financials", baseline_score: 22.7, scenario_score: 35.1, delta: 12.4, direction_change: false },
      { symbol: "XLE", name: "Energy", baseline_score: -12.4, scenario_score: 18.5, delta: 30.9, direction_change: true },
      { symbol: "XLU", name: "Utilities", baseline_score: -28.3, scenario_score: -15.1, delta: 13.2, direction_change: false },
    ],
    watchlist_impacts: [
      { symbol: "NVDA", name: "NVIDIA", baseline_signal: 66.8, scenario_signal: 35.2, delta: -31.6, label_change: "strong_tailwind → tailwind" },
      { symbol: "JPM", name: "JPMorgan Chase", baseline_signal: 12.4, scenario_signal: 28.3, delta: 15.9, label_change: "mixed → tailwind" },
      { symbol: "XOM", name: "Exxon Mobil", baseline_signal: -13.2, scenario_signal: 15.8, delta: 29.0, label_change: "headwind → tailwind" },
    ],
    uncertainty_notes: [
      "Simulation based on historical pattern matching. Actual outcomes may differ.",
      "Cross-asset correlations may shift under stress conditions.",
    ],
  };
}
