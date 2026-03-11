"""Tests for sector scoring engine."""

from __future__ import annotations

from investorframe.core.config import AppConfig
from investorframe.core.models import Event, MarketRegime, SectorScore
from investorframe.core.types import Direction, RegimeState
from investorframe.sectors.engine import SectorScoringEngine


class TestSectorScoringEngine:
    def test_score_all_with_events(
        self,
        config: AppConfig,
        mock_events: list[Event],
        mock_regime_risk_on: MarketRegime,
    ) -> None:
        engine = SectorScoringEngine(config)
        scores = engine.score_all(mock_events, mock_regime_risk_on)
        assert len(scores) > 0
        # All scores should be SectorScore instances
        for s in scores:
            assert isinstance(s, SectorScore)
            assert -100 <= s.score <= 100

    def test_score_all_empty_events(
        self, config: AppConfig, mock_regime_risk_on: MarketRegime
    ) -> None:
        engine = SectorScoringEngine(config)
        scores = engine.score_all([], mock_regime_risk_on)
        assert len(scores) > 0
        # All scores should be 0 or near 0 with no events
        for s in scores:
            assert s.score == 0.0

    def test_scores_are_ranked(
        self,
        config: AppConfig,
        mock_events: list[Event],
        mock_regime_risk_on: MarketRegime,
    ) -> None:
        engine = SectorScoringEngine(config)
        scores = engine.score_all(mock_events, mock_regime_risk_on)
        ranks = [s.rank for s in scores]
        assert ranks == sorted(ranks)
        assert ranks[0] == 1

    def test_regime_modifier_applied(
        self,
        config: AppConfig,
        mock_events: list[Event],
    ) -> None:
        engine = SectorScoringEngine(config)
        risk_on = MarketRegime(state=RegimeState.RISK_ON, confidence=0.9)
        risk_off = MarketRegime(state=RegimeState.RISK_OFF, confidence=0.9)

        scores_on = {s.symbol: s.score for s in engine.score_all(mock_events, risk_on)}
        scores_off = {s.symbol: s.score for s in engine.score_all(mock_events, risk_off)}

        # At least some sectors should differ between regimes
        differences = [
            abs(scores_on.get(sym, 0) - scores_off.get(sym, 0))
            for sym in scores_on
        ]
        assert any(d > 0 for d in differences)

    def test_confidence_between_0_and_1(
        self,
        config: AppConfig,
        mock_events: list[Event],
        mock_regime_risk_on: MarketRegime,
    ) -> None:
        engine = SectorScoringEngine(config)
        scores = engine.score_all(mock_events, mock_regime_risk_on)
        for s in scores:
            assert 0.0 <= s.confidence <= 1.0
