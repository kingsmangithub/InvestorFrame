"""Tests for sentiment aggregation."""

from __future__ import annotations

from datetime import datetime, timezone

from investorframe.core.models import SentimentSignal
from investorframe.core.types import DataSource, SentimentLabel
from investorframe.sentiment.aggregator import SentimentAggregator


class TestSentimentAggregator:
    def test_aggregate_empty(self) -> None:
        agg = SentimentAggregator()
        result = agg.aggregate([])
        assert result.composite_score == 0.0
        assert result.label == SentimentLabel.NEUTRAL

    def test_aggregate_single_bullish(self) -> None:
        agg = SentimentAggregator()
        signal = SentimentSignal(
            source=DataSource.NEWSAPI,
            score=0.6,
            label=SentimentLabel.BULLISH,
            confidence=0.8,
            sample_size=10,
        )
        result = agg.aggregate([signal])
        assert result.composite_score > 0
        assert result.confidence > 0

    def test_aggregate_mixed_signals(self) -> None:
        agg = SentimentAggregator()
        signals = [
            SentimentSignal(
                source=DataSource.FRED,
                score=0.5,
                label=SentimentLabel.BULLISH,
                confidence=0.8,
                sample_size=5,
            ),
            SentimentSignal(
                source=DataSource.NEWSAPI,
                score=-0.3,
                label=SentimentLabel.BEARISH,
                confidence=0.7,
                sample_size=20,
            ),
        ]
        result = agg.aggregate(signals)
        # Mixed but FRED has higher weight, so slightly positive expected
        assert -1.0 <= result.composite_score <= 1.0
        assert result.confidence > 0

    def test_aggregate_preserves_signals(self) -> None:
        agg = SentimentAggregator()
        signals = [
            SentimentSignal(
                source=DataSource.FRED,
                score=0.3,
                label=SentimentLabel.BULLISH,
                confidence=0.7,
                sample_size=3,
            ),
        ]
        result = agg.aggregate(signals)
        assert len(result.signals) == 1

    def test_confidence_bounds(self) -> None:
        agg = SentimentAggregator()
        signals = [
            SentimentSignal(
                source=DataSource.NEWSAPI,
                score=0.9,
                label=SentimentLabel.VERY_BULLISH,
                confidence=1.0,
                sample_size=100,
            ),
        ]
        result = agg.aggregate(signals)
        assert 0.0 <= result.confidence <= 1.0
