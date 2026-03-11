"""Pydantic domain models for InvestorFrame.

All models use Pydantic v2 conventions with frozen base for immutability
across the pipeline.
"""

from __future__ import annotations

import uuid
from datetime import date, datetime, timezone
from typing import Any

from pydantic import BaseModel, Field, computed_field, field_validator

from investorframe.core.types import (
    Confidence,
    DataSource,
    Direction,
    EventSubtype,
    EventType,
    PipelineStatus,
    RegimeState,
    Score,
    SectorSymbol,
    SentimentLabel,
    Severity,
    SignalLabel,
    StockSymbol,
    Weight,
)


# ── Base ──────────────────────────────────────────────────────


class _FrozenBase(BaseModel):
    """Shared base with immutability."""

    model_config = {
        "frozen": True,
        "str_strip_whitespace": True,
        "validate_default": True,
        "populate_by_name": True,
    }


# ═══════════════════════════════════════════════════════════════
# Raw Data Models (Connector Output)
# ═══════════════════════════════════════════════════════════════


class RawNewsArticle(_FrozenBase):
    """Raw article from NewsAPI before classification."""

    title: str = Field(..., min_length=1)
    description: str | None = None
    content: str | None = None
    source_name: str = Field(..., min_length=1)
    url: str = Field(..., min_length=1)
    published_at: datetime
    raw_json: dict[str, Any] = Field(default_factory=dict)

    @field_validator("published_at", mode="before")
    @classmethod
    def _ensure_utc(cls, v: datetime) -> datetime:
        if isinstance(v, str):
            v = datetime.fromisoformat(v)
        if v.tzinfo is None:
            return v.replace(tzinfo=timezone.utc)
        return v


class EconomicDataPoint(_FrozenBase):
    """Single data point from FRED."""

    series_id: str = Field(..., min_length=1)
    series_name: str = Field(..., min_length=1)
    value: float
    date: date
    previous_value: float | None = None
    change_pct: float | None = None
    unit: str = "index"


class MarketSnapshot(_FrozenBase):
    """Market data snapshot from yfinance."""

    symbol: str = Field(..., min_length=1)
    price: float = Field(..., gt=0)
    change_pct: float
    volume: int = Field(..., ge=0)
    fifty_day_ma: float | None = None
    two_hundred_day_ma: float | None = None
    vix: float | None = None
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
    )


# ═══════════════════════════════════════════════════════════════
# Core Pipeline Models
# ═══════════════════════════════════════════════════════════════


class Event(_FrozenBase):
    """A classified market event flowing through the pipeline.

    Events carry severity, confidence, and ttl_days that together
    drive time-weighted scoring through effective_severity.
    """

    id: str = Field(default_factory=lambda: uuid.uuid4().hex[:12])
    event_type: EventType
    subtype: EventSubtype
    source: DataSource
    timestamp: datetime
    severity: Severity
    direction: Direction
    confidence: Confidence = Field(ge=0.0, le=1.0)
    headline: str = Field(..., min_length=1)
    summary: str = ""
    raw_text: str = ""
    metadata: dict[str, Any] = Field(default_factory=dict)
    ttl_days: int = Field(default=7, ge=1, le=90)

    @field_validator("confidence")
    @classmethod
    def _clamp_confidence(cls, v: float) -> float:
        return round(max(0.0, min(1.0, v)), 4)

    @field_validator("timestamp", mode="before")
    @classmethod
    def _ensure_utc(cls, v: datetime) -> datetime:
        if isinstance(v, str):
            v = datetime.fromisoformat(v)
        if v.tzinfo is None:
            return v.replace(tzinfo=timezone.utc)
        return v

    @computed_field  # type: ignore[prop-decorator]
    @property
    def age_days(self) -> float:
        delta = datetime.now(timezone.utc) - self.timestamp
        return max(delta.total_seconds() / 86_400, 0.0)

    @computed_field  # type: ignore[prop-decorator]
    @property
    def decay_factor(self) -> float:
        """Linear decay: 1.0 at creation, 0.0 at ttl expiry."""
        return max(1.0 - (self.age_days / self.ttl_days), 0.0)

    @computed_field  # type: ignore[prop-decorator]
    @property
    def effective_severity(self) -> float:
        """Time-and-confidence-weighted severity for scoring."""
        return round(self.severity.value * self.confidence * self.decay_factor, 4)


# ═══════════════════════════════════════════════════════════════
# Sentiment Models
# ═══════════════════════════════════════════════════════════════


class SentimentSignal(_FrozenBase):
    """A single sentiment reading from one source."""

    source: DataSource
    score: float = Field(ge=-1.0, le=1.0)
    label: SentimentLabel
    confidence: Confidence = Field(ge=0.0, le=1.0)
    sample_size: int = Field(default=1, ge=1)
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
    )


class AggregateSentiment(_FrozenBase):
    """Weighted aggregate of multiple sentiment signals."""

    composite_score: float = Field(ge=-1.0, le=1.0)
    label: SentimentLabel
    confidence: Confidence = Field(ge=0.0, le=1.0)
    signals: list[SentimentSignal] = Field(default_factory=list)
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
    )


# ═══════════════════════════════════════════════════════════════
# Market Regime
# ═══════════════════════════════════════════════════════════════


class MarketRegime(_FrozenBase):
    """Current detected market regime."""

    state: RegimeState
    confidence: Confidence = Field(ge=0.0, le=1.0)
    contributing_factors: list[str] = Field(default_factory=list)
    indicator_values: dict[str, float] = Field(default_factory=dict)
    previous_state: RegimeState | None = None
    state_duration_days: int = Field(default=0, ge=0)
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
    )


# ═══════════════════════════════════════════════════════════════
# Scoring Models
# ═══════════════════════════════════════════════════════════════


class EventContribution(_FrozenBase):
    """How a single event contributed to a score."""

    event_id: str = Field(..., min_length=1)
    headline: str = Field(..., min_length=1)
    direction: Direction
    contribution: float
    weight: Weight


class SectorScore(_FrozenBase):
    """Scored sector with explanatory detail."""

    symbol: SectorSymbol = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    score: Score = Field(ge=-100.0, le=100.0)
    direction: Direction
    confidence: Confidence = Field(ge=0.0, le=1.0)
    rank: int = Field(default=0, ge=0)
    driving_events: list[EventContribution] = Field(default_factory=list)
    regime_modifier: float = 1.0
    raw_score: float = 0.0
    event_count: int = Field(default=0, ge=0)
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
    )

    @field_validator("score")
    @classmethod
    def _clamp_score(cls, v: float) -> float:
        return round(max(-100.0, min(100.0, v)), 2)


class StockScore(_FrozenBase):
    """Scored watchlist stock with full explanation."""

    symbol: StockSymbol = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    sector: SectorSymbol = Field(..., min_length=1)
    sector_name: str = Field(..., min_length=1)
    tailwind_score: Score = Field(ge=0.0, le=100.0)
    headwind_score: Score = Field(ge=0.0, le=100.0)
    net_signal: Score = Field(ge=-100.0, le=100.0)
    label: SignalLabel
    confidence: Confidence = Field(ge=0.0, le=1.0)
    explanation: str = ""
    driving_events: list[EventContribution] = Field(default_factory=list)
    sector_score_contribution: float = 0.0
    rank: int = Field(default=0, ge=0)
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
    )

    @field_validator("net_signal")
    @classmethod
    def _clamp_net_signal(cls, v: float) -> float:
        return round(max(-100.0, min(100.0, v)), 2)


# ═══════════════════════════════════════════════════════════════
# Scenario Models
# ═══════════════════════════════════════════════════════════════


class ScenarioEvent(_FrozenBase):
    """A synthetic event injected by a scenario."""

    event_type: EventType
    subtype: EventSubtype
    severity: Severity
    direction: Direction
    headline: str = Field(..., min_length=1)
    confidence: Confidence = 0.8


class ScenarioTemplate(_FrozenBase):
    """A predefined what-if scenario."""

    name: str = Field(..., min_length=1)
    description: str = ""
    events: list[ScenarioEvent] = Field(..., min_length=1)
    regime_override: RegimeState | None = None


class SectorImpact(_FrozenBase):
    """How a scenario changes a sector score."""

    symbol: SectorSymbol = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    baseline_score: Score
    scenario_score: Score
    delta: float
    direction_change: bool = False


class WatchlistImpact(_FrozenBase):
    """How a scenario changes a stock score."""

    symbol: StockSymbol = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    baseline_net_signal: Score
    scenario_net_signal: Score
    delta: float
    label_change: str | None = None


class ScenarioResult(_FrozenBase):
    """Complete result of a scenario simulation."""

    scenario_name: str = Field(..., min_length=1)
    description: str = ""
    regime_impact: dict[str, Any] = Field(default_factory=dict)
    sector_impacts: list[SectorImpact] = Field(default_factory=list)
    watchlist_impacts: list[WatchlistImpact] = Field(default_factory=list)
    uncertainty_notes: list[str] = Field(default_factory=list)
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
    )


# ═══════════════════════════════════════════════════════════════
# Risk & Output Models
# ═══════════════════════════════════════════════════════════════


class RiskFlag(_FrozenBase):
    """A risk gate flag raised during validation."""

    code: str = Field(..., min_length=1)
    severity: Severity
    message: str = Field(..., min_length=1)
    affected_symbols: list[str] = Field(default_factory=list)


class RiskAssessment(_FrozenBase):
    """Result of running all risk gates."""

    passed: bool
    flags: list[RiskFlag] = Field(default_factory=list)
    disclaimers: list[str] = Field(default_factory=list)
    data_freshness: dict[str, datetime] = Field(default_factory=dict)
    confidence_floor: Confidence = 0.0


class PipelineResult(_FrozenBase):
    """Complete output of a single pipeline run."""

    run_id: str = Field(default_factory=lambda: uuid.uuid4().hex[:16])
    status: PipelineStatus
    started_at: datetime
    completed_at: datetime | None = None
    duration_seconds: float = Field(default=0.0, ge=0)

    events: list[Event] = Field(default_factory=list)
    sentiment: AggregateSentiment | None = None
    regime: MarketRegime | None = None
    sector_scores: list[SectorScore] = Field(default_factory=list)
    stock_scores: list[StockScore] = Field(default_factory=list)
    risk_assessment: RiskAssessment | None = None

    warnings: list[str] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)
    connector_status: dict[str, str] = Field(default_factory=dict)
