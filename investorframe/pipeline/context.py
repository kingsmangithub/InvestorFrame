"""Mutable state carrier passed through pipeline phases."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any

from investorframe.core.models import (
    AggregateSentiment,
    EconomicDataPoint,
    Event,
    MarketRegime,
    MarketSnapshot,
    PipelineResult,
    RawNewsArticle,
    RiskAssessment,
    SectorScore,
    StockScore,
)
from investorframe.core.types import PipelineStatus


class PipelineContext:
    """Accumulates state across pipeline phases.

    Each phase writes its outputs into the context, and the next phase
    reads what it needs.  At the end, ``to_result()`` freezes everything
    into an immutable ``PipelineResult``.
    """

    def __init__(self, run_id: str | None = None) -> None:
        self.run_id = run_id or uuid.uuid4().hex[:16]
        self.started_at = datetime.now(timezone.utc)
        self.status = PipelineStatus.RUNNING

        # Phase 1: Raw data from connectors
        self.raw_articles: list[RawNewsArticle] = []
        self.economic_data: list[EconomicDataPoint] = []
        self.market_data: list[MarketSnapshot] = []

        # Phase 2: Classified events
        self.events: list[Event] = []

        # Phase 3: Market state
        self.sentiment: AggregateSentiment | None = None
        self.regime: MarketRegime | None = None

        # Phase 4: Scores
        self.sector_scores: list[SectorScore] = []
        self.stock_scores: list[StockScore] = []

        # Phase 5: Risk assessment
        self.risk_assessment: RiskAssessment | None = None

        # Diagnostics
        self.warnings: list[str] = []
        self.errors: list[str] = []
        self.connector_status: dict[str, str] = {}

    def to_result(self) -> PipelineResult:
        """Freeze mutable context into an immutable PipelineResult."""
        completed_at = datetime.now(timezone.utc)
        return PipelineResult(
            run_id=self.run_id,
            status=self.status,
            started_at=self.started_at,
            completed_at=completed_at,
            duration_seconds=round(
                (completed_at - self.started_at).total_seconds(), 3
            ),
            events=self.events,
            sentiment=self.sentiment,
            regime=self.regime,
            sector_scores=self.sector_scores,
            stock_scores=self.stock_scores,
            risk_assessment=self.risk_assessment,
            warnings=self.warnings,
            errors=self.errors,
            connector_status=self.connector_status,
        )

    def add_warning(self, msg: str) -> None:
        self.warnings.append(msg)

    def add_error(self, msg: str) -> None:
        self.errors.append(msg)
