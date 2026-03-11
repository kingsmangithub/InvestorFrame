"""Risk gate validation for pipeline outputs."""

from __future__ import annotations

import logging
from datetime import datetime, timedelta, timezone

from investorframe.core.config import AppConfig
from investorframe.core.models import (
    MarketRegime,
    PipelineResult,
    RiskAssessment,
    RiskFlag,
    SectorScore,
)
from investorframe.core.types import RegimeState, Severity

logger = logging.getLogger(__name__)


class RiskGateRunner:
    """Validates pipeline output against risk gates."""

    def __init__(self, config: AppConfig) -> None:
        self.config = config
        self.confidence_floor = config.pipeline.confidence_floor

    def assess(
        self,
        result: PipelineResult,
    ) -> RiskAssessment:
        """Run all risk gates and return assessment."""
        flags: list[RiskFlag] = []
        data_freshness: dict[str, datetime] = {}

        # Gate 1: Data freshness
        self._check_data_freshness(result, flags, data_freshness)

        # Gate 2: Confidence floor
        self._check_confidence_floor(result, flags)

        # Gate 3: Event coverage
        self._check_event_coverage(result, flags)

        # Gate 4: Regime stability
        self._check_regime_stability(result, flags)

        # Gate 5: Connector failures
        self._check_connector_failures(result, flags)

        # Gate 6: Score extremes
        self._check_score_extremes(result, flags)

        # Determine overall pass/fail
        critical_flags = [f for f in flags if f.severity == Severity.CRITICAL]
        passed = len(critical_flags) == 0

        # Generate disclaimers
        from investorframe.risk.disclaimers import DisclaimerGenerator

        disclaimers = DisclaimerGenerator().generate(flags, result.regime)

        min_confidence = self._find_min_confidence(result)

        return RiskAssessment(
            passed=passed,
            flags=flags,
            disclaimers=disclaimers,
            data_freshness=data_freshness,
            confidence_floor=min_confidence,
        )

    def _check_data_freshness(
        self,
        result: PipelineResult,
        flags: list[RiskFlag],
        freshness: dict[str, datetime],
    ) -> None:
        """Flag if any data source is stale."""
        max_age = timedelta(days=self.config.pipeline.lookback_days)
        now = datetime.now(timezone.utc)

        if result.events:
            latest_event = max(result.events, key=lambda e: e.timestamp)
            freshness["events"] = latest_event.timestamp
            if now - latest_event.timestamp > max_age:
                flags.append(
                    RiskFlag(
                        code="STALE_EVENTS",
                        severity=Severity.HIGH,
                        message=f"Latest event is {(now - latest_event.timestamp).days} days old",
                    )
                )

    def _check_confidence_floor(
        self, result: PipelineResult, flags: list[RiskFlag]
    ) -> None:
        """Flag scores below confidence floor."""
        for sector in result.sector_scores:
            if sector.confidence < self.confidence_floor:
                flags.append(
                    RiskFlag(
                        code="LOW_CONFIDENCE",
                        severity=Severity.MODERATE,
                        message=f"Sector {sector.symbol} confidence {sector.confidence:.2f} below floor {self.confidence_floor}",
                        affected_symbols=[sector.symbol],
                    )
                )

    def _check_event_coverage(
        self, result: PipelineResult, flags: list[RiskFlag]
    ) -> None:
        """Flag if too few events were collected."""
        if len(result.events) < 5:
            flags.append(
                RiskFlag(
                    code="LOW_EVENT_COVERAGE",
                    severity=Severity.HIGH,
                    message=f"Only {len(result.events)} events collected (minimum recommended: 5)",
                )
            )

    def _check_regime_stability(
        self, result: PipelineResult, flags: list[RiskFlag]
    ) -> None:
        """Flag TRANSITION regime with low confidence."""
        if result.regime and result.regime.state == RegimeState.TRANSITION:
            if result.regime.confidence < 0.5:
                flags.append(
                    RiskFlag(
                        code="UNSTABLE_REGIME",
                        severity=Severity.HIGH,
                        message=f"Market regime in TRANSITION with low confidence ({result.regime.confidence:.2f})",
                    )
                )

    def _check_connector_failures(
        self, result: PipelineResult, flags: list[RiskFlag]
    ) -> None:
        """Flag any failed connectors."""
        for connector, status in result.connector_status.items():
            if status not in ("ok", "healthy"):
                flags.append(
                    RiskFlag(
                        code="CONNECTOR_FAILURE",
                        severity=Severity.HIGH,
                        message=f"Connector '{connector}' status: {status}",
                    )
                )

    def _check_score_extremes(
        self, result: PipelineResult, flags: list[RiskFlag]
    ) -> None:
        """Flag scores with |score| > 90 as possible anomalies."""
        for sector in result.sector_scores:
            if abs(sector.score) > 90:
                flags.append(
                    RiskFlag(
                        code="EXTREME_SCORE",
                        severity=Severity.MODERATE,
                        message=f"Sector {sector.symbol} has extreme score {sector.score:+.1f}",
                        affected_symbols=[sector.symbol],
                    )
                )

    def _find_min_confidence(self, result: PipelineResult) -> float:
        """Find the minimum confidence across all outputs."""
        confidences = []
        if result.regime:
            confidences.append(result.regime.confidence)
        if result.sentiment:
            confidences.append(result.sentiment.confidence)
        for s in result.sector_scores:
            confidences.append(s.confidence)
        for s in result.stock_scores:
            confidences.append(s.confidence)
        return min(confidences) if confidences else 0.0
