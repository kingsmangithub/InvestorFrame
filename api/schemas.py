"""API response models for InvestorFrame."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, Field


# ── Response Envelope ────────────────────────────────────────


class APIMetadata(BaseModel):
    pipeline_run_id: str = ""
    data_freshness: datetime | None = None
    warnings: list[str] = Field(default_factory=list)


class APIResponse(BaseModel):
    status: str = "ok"
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    data: Any = None
    meta: APIMetadata | None = None
    error: str | None = None


# ── Health ───────────────────────────────────────────────────


class ConnectorHealth(BaseModel):
    name: str
    status: str
    last_success: datetime | None = None


class HealthData(BaseModel):
    version: str
    uptime_seconds: float
    last_pipeline_run: datetime | None = None
    last_pipeline_status: str | None = None
    connectors: list[ConnectorHealth] = Field(default_factory=list)
    database_status: str = "ok"


# ── Market ───────────────────────────────────────────────────


class MarketEventSummary(BaseModel):
    id: str
    event_type: str
    subtype: str
    severity: int
    direction: str
    headline: str
    confidence: float
    timestamp: datetime
    age_hours: float


class MarketData(BaseModel):
    regime: dict[str, Any] | None = None
    sentiment: dict[str, Any] | None = None
    active_events: list[MarketEventSummary] = Field(default_factory=list)
    event_count: int = 0


# ── Sectors ──────────────────────────────────────────────────


class SectorSummary(BaseModel):
    symbol: str
    name: str
    score: float
    direction: str
    confidence: float
    rank: int
    event_count: int
    top_drivers: list[str] = Field(default_factory=list)


class SectorsData(BaseModel):
    sectors: list[SectorSummary] = Field(default_factory=list)
    regime_state: str = "unknown"
    regime_confidence: float = 0.0
    total_sectors: int = 0


# ── Watchlist ────────────────────────────────────────────────


class StockSummary(BaseModel):
    symbol: str
    name: str
    sector: str
    sector_name: str
    tailwind_score: float
    headwind_score: float
    net_signal: float
    label: str
    confidence: float
    explanation: str
    rank: int
    top_drivers: list[str] = Field(default_factory=list)


class WatchlistData(BaseModel):
    stocks: list[StockSummary] = Field(default_factory=list)
    total_stocks: int = 0
    tailwind_count: int = 0
    headwind_count: int = 0
    mixed_count: int = 0


# ── Scenarios ────────────────────────────────────────────────


class ScenarioRequest(BaseModel):
    scenario_name: str | None = None
    custom_events: list[dict[str, Any]] | None = None
    description: str = ""
    regime_override: str | None = None


class ScenarioSectorDelta(BaseModel):
    symbol: str
    name: str
    baseline_score: float
    scenario_score: float
    delta: float
    direction_change: bool = False


class ScenarioStockDelta(BaseModel):
    symbol: str
    name: str
    baseline_signal: float
    scenario_signal: float
    delta: float
    label_change: str | None = None


class ScenarioData(BaseModel):
    scenario_name: str
    description: str
    regime_impact: dict[str, Any] = Field(default_factory=dict)
    sector_impacts: list[ScenarioSectorDelta] = Field(default_factory=list)
    watchlist_impacts: list[ScenarioStockDelta] = Field(default_factory=list)
    uncertainty_notes: list[str] = Field(default_factory=list)
