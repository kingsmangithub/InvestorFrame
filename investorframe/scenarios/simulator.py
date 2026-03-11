"""What-if scenario simulation engine."""

from __future__ import annotations

import logging
from datetime import datetime, timezone

from investorframe.core.config import AppConfig
from investorframe.core.models import (
    Event,
    MarketRegime,
    ScenarioResult,
    ScenarioTemplate,
    SectorImpact,
    SectorScore,
    StockScore,
    WatchlistImpact,
)
from investorframe.core.types import DataSource, RegimeState
from investorframe.sectors.engine import SectorScoringEngine
from investorframe.watchlist.scorer import StockScorer

logger = logging.getLogger(__name__)


class ScenarioSimulator:
    """Injects synthetic events and computes scoring deltas vs baseline."""

    def __init__(self, config: AppConfig) -> None:
        self.config = config
        self.sector_engine = SectorScoringEngine(config)
        self.stock_scorer = StockScorer(config)

    def simulate(
        self,
        template: ScenarioTemplate,
        baseline_events: list[Event],
        baseline_regime: MarketRegime | None = None,
        baseline_sectors: list[SectorScore] | None = None,
        baseline_stocks: list[StockScore] | None = None,
    ) -> ScenarioResult:
        """Run a scenario simulation and compute deltas."""

        # 1. Convert scenario events to pipeline Events
        synthetic_events = self._create_synthetic_events(template)

        # 2. Combine with baseline events
        combined_events = list(baseline_events) + synthetic_events

        # 3. Determine regime for scenario
        scenario_regime = baseline_regime
        if template.regime_override is not None and scenario_regime is not None:
            scenario_regime = MarketRegime(
                state=template.regime_override,
                confidence=0.9,
                contributing_factors=[f"Scenario override: {template.name}"],
                indicator_values=scenario_regime.indicator_values,
            )

        # 4. Re-score sectors with scenario events
        scenario_sectors = self.sector_engine.score_all(combined_events, scenario_regime)

        # 5. Compute sector deltas
        sector_impacts = self._compute_sector_impacts(
            baseline_sectors or [], scenario_sectors
        )

        # 6. Re-score watchlist
        scenario_stocks = self.stock_scorer.score_all(scenario_sectors)

        # 7. Compute stock deltas
        watchlist_impacts = self._compute_watchlist_impacts(
            baseline_stocks or [], scenario_stocks
        )

        # 8. Regime impact
        regime_impact = {}
        if baseline_regime and scenario_regime:
            regime_impact = {
                "baseline_state": baseline_regime.state.value,
                "scenario_state": scenario_regime.state.value,
                "state_changed": baseline_regime.state != scenario_regime.state,
                "confidence_delta": round(
                    scenario_regime.confidence - baseline_regime.confidence, 4
                ),
            }

        # 9. Uncertainty notes
        uncertainty_notes = [
            "Scenario analysis is based on simplified models and historical patterns.",
            "Actual market reactions may differ significantly from modeled outcomes.",
            f"This scenario injects {len(synthetic_events)} synthetic event(s).",
        ]

        return ScenarioResult(
            scenario_name=template.name,
            description=template.description,
            regime_impact=regime_impact,
            sector_impacts=sector_impacts,
            watchlist_impacts=watchlist_impacts,
            uncertainty_notes=uncertainty_notes,
        )

    def _create_synthetic_events(self, template: ScenarioTemplate) -> list[Event]:
        """Convert ScenarioEvents to full Event objects."""
        events = []
        for se in template.events:
            events.append(
                Event(
                    event_type=se.event_type,
                    subtype=se.subtype,
                    source=DataSource.SCENARIO,
                    timestamp=datetime.now(timezone.utc),
                    severity=se.severity,
                    direction=se.direction,
                    confidence=se.confidence,
                    headline=se.headline,
                    summary=f"Scenario: {template.name}",
                    metadata={"scenario": template.name},
                )
            )
        return events

    def _compute_sector_impacts(
        self,
        baseline: list[SectorScore],
        scenario: list[SectorScore],
    ) -> list[SectorImpact]:
        """Compute per-sector deltas."""
        baseline_map = {s.symbol: s for s in baseline}
        impacts = []
        for ss in scenario:
            bs = baseline_map.get(ss.symbol)
            baseline_score = bs.score if bs else 0.0
            delta = round(ss.score - baseline_score, 4)
            direction_changed = (
                bs is not None and bs.direction != ss.direction
            )
            impacts.append(
                SectorImpact(
                    symbol=ss.symbol,
                    name=ss.name,
                    baseline_score=baseline_score,
                    scenario_score=ss.score,
                    delta=delta,
                    direction_change=direction_changed,
                )
            )
        impacts.sort(key=lambda x: abs(x.delta), reverse=True)
        return impacts

    def _compute_watchlist_impacts(
        self,
        baseline: list[StockScore],
        scenario: list[StockScore],
    ) -> list[WatchlistImpact]:
        """Compute per-stock deltas."""
        baseline_map = {s.symbol: s for s in baseline}
        impacts = []
        for ss in scenario:
            bs = baseline_map.get(ss.symbol)
            baseline_signal = bs.net_signal if bs else 0.0
            delta = round(ss.net_signal - baseline_signal, 4)
            label_change = None
            if bs is not None and bs.label != ss.label:
                label_change = f"{bs.label.value} -> {ss.label.value}"
            impacts.append(
                WatchlistImpact(
                    symbol=ss.symbol,
                    name=ss.name,
                    baseline_net_signal=baseline_signal,
                    scenario_net_signal=ss.net_signal,
                    delta=delta,
                    label_change=label_change,
                )
            )
        impacts.sort(key=lambda x: abs(x.delta), reverse=True)
        return impacts
