// ── API Response Envelope ─────────────────────────────────

export interface APIResponse<T = unknown> {
  status: string;
  timestamp: string;
  data: T;
  meta: {
    pipeline_run_id: string;
    data_freshness: string | null;
    warnings: string[];
  } | null;
  error: string | null;
}

// ── Market ────────────────────────────────────────────────

export interface MarketEventSummary {
  id: string;
  event_type: string;
  subtype: string;
  severity: number;
  direction: string;
  headline: string;
  confidence: number;
  timestamp: string;
  age_hours: number;
}

export interface MarketData {
  regime: {
    state: string;
    confidence: number;
    contributing_factors: string[];
    indicator_values: Record<string, number>;
  } | null;
  sentiment: {
    composite_score: number;
    label: string;
    confidence: number;
  } | null;
  active_events: MarketEventSummary[];
  event_count: number;
}

// ── Sectors ───────────────────────────────────────────────

export interface SectorSummary {
  symbol: string;
  name: string;
  score: number;
  direction: string;
  confidence: number;
  rank: number;
  event_count: number;
  top_drivers: string[];
}

export interface SectorsData {
  sectors: SectorSummary[];
  regime_state: string;
  regime_confidence: number;
  total_sectors: number;
}

// ── Watchlist ─────────────────────────────────────────────

export interface StockSummary {
  symbol: string;
  name: string;
  sector: string;
  sector_name: string;
  tailwind_score: number;
  headwind_score: number;
  net_signal: number;
  label: string;
  confidence: number;
  explanation: string;
  rank: number;
  top_drivers: string[];
}

export interface WatchlistData {
  stocks: StockSummary[];
  total_stocks: number;
  tailwind_count: number;
  headwind_count: number;
  mixed_count: number;
}

// ── Scenarios ─────────────────────────────────────────────

export interface ScenarioRequest {
  scenario_name: string;
}

export interface ScenarioSectorDelta {
  symbol: string;
  name: string;
  baseline_score: number;
  scenario_score: number;
  delta: number;
  direction_change: boolean;
}

export interface ScenarioStockDelta {
  symbol: string;
  name: string;
  baseline_signal: number;
  scenario_signal: number;
  delta: number;
  label_change: string | null;
}

export interface ScenarioData {
  scenario_name: string;
  description: string;
  regime_impact: Record<string, unknown>;
  sector_impacts: ScenarioSectorDelta[];
  watchlist_impacts: ScenarioStockDelta[];
  uncertainty_notes: string[];
}

// ── Health ─────────────────────────────────────────────────

export interface HealthData {
  version: string;
  uptime_seconds: number;
  last_pipeline_run: string | null;
  last_pipeline_status: string | null;
  database_status: string;
}
