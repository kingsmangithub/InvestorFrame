"""Tests for watchlist stock scorer."""

from __future__ import annotations

from investorframe.core.config import AppConfig
from investorframe.core.models import SectorScore, StockScore
from investorframe.core.types import SignalLabel
from investorframe.watchlist.scorer import StockScorer


class TestStockScorer:
    def test_score_all(
        self, config: AppConfig, mock_sector_scores: list[SectorScore]
    ) -> None:
        scorer = StockScorer(config)
        stocks = scorer.score_all(mock_sector_scores)
        assert len(stocks) > 0
        for s in stocks:
            assert isinstance(s, StockScore)
            assert -100 <= s.net_signal <= 100

    def test_scores_are_ranked(
        self, config: AppConfig, mock_sector_scores: list[SectorScore]
    ) -> None:
        scorer = StockScorer(config)
        stocks = scorer.score_all(mock_sector_scores)
        ranks = [s.rank for s in stocks]
        assert ranks == sorted(ranks)
        if ranks:
            assert ranks[0] == 1

    def test_label_assignment(
        self, config: AppConfig, mock_sector_scores: list[SectorScore]
    ) -> None:
        scorer = StockScorer(config)
        stocks = scorer.score_all(mock_sector_scores)
        valid_labels = {
            SignalLabel.STRONG_TAILWIND,
            SignalLabel.TAILWIND,
            SignalLabel.NEUTRAL,
            SignalLabel.MIXED,
            SignalLabel.HEADWIND,
            SignalLabel.STRONG_HEADWIND,
        }
        for s in stocks:
            assert s.label in valid_labels

    def test_beta_amplification(self, config: AppConfig) -> None:
        scorer = StockScorer(config)
        # NVDA has beta 1.65, MSFT has beta 0.95
        # Same sector (XLK) so different beta should produce different signals
        from investorframe.core.models import EventContribution
        from investorframe.core.types import Direction

        sector_scores = [
            SectorScore(
                symbol="XLK",
                name="Technology",
                score=50.0,
                direction=Direction.BULLISH,
                confidence=0.8,
                rank=1,
            ),
        ]
        stocks = scorer.score_all(sector_scores)
        tech_stocks = {s.symbol: s for s in stocks if s.sector == "XLK"}

        if "NVDA" in tech_stocks and "MSFT" in tech_stocks:
            # NVDA (beta 1.65) should have larger signal than MSFT (beta 0.95)
            assert abs(tech_stocks["NVDA"].net_signal) > abs(tech_stocks["MSFT"].net_signal)

    def test_explanation_generated(
        self, config: AppConfig, mock_sector_scores: list[SectorScore]
    ) -> None:
        scorer = StockScorer(config)
        stocks = scorer.score_all(mock_sector_scores)
        for s in stocks:
            assert len(s.explanation) > 0
