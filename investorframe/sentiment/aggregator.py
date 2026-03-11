"""Weighted sentiment aggregation across multiple signals."""

from __future__ import annotations

from datetime import datetime, timezone

from investorframe.core.models import AggregateSentiment, SentimentSignal
from investorframe.core.types import SentimentLabel


class SentimentAggregator:
    """Combines multiple sentiment signals into a weighted composite."""

    SOURCE_WEIGHTS: dict[str, float] = {
        "fred": 0.35,
        "newsapi": 0.25,
        "yfinance": 0.30,
        "openai": 0.10,
    }

    def aggregate(
        self,
        signals: list[SentimentSignal],
        weights: dict[str, float] | None = None,
    ) -> AggregateSentiment:
        """Compute weighted average of sentiment signals."""
        if not signals:
            return AggregateSentiment(
                composite_score=0.0,
                label=SentimentLabel.NEUTRAL,
                confidence=0.0,
                signals=[],
            )

        w = weights or self.SOURCE_WEIGHTS
        composite = self._weighted_mean(signals, w)
        confidence = self._composite_confidence(signals)

        label = self._score_to_label(composite)

        return AggregateSentiment(
            composite_score=round(composite, 4),
            label=label,
            confidence=round(confidence, 4),
            signals=signals,
        )

    def _weighted_mean(
        self,
        signals: list[SentimentSignal],
        weights: dict[str, float],
    ) -> float:
        """Calculate confidence-weighted mean score."""
        total_weight = 0.0
        weighted_sum = 0.0

        for signal in signals:
            source_weight = weights.get(signal.source.value, 0.1)
            effective_weight = source_weight * signal.confidence
            # Scale by sample size (diminishing returns)
            sample_factor = min(1.0, signal.sample_size / 10.0)
            effective_weight *= (0.5 + 0.5 * sample_factor)

            weighted_sum += signal.score * effective_weight
            total_weight += effective_weight

        if total_weight == 0:
            return 0.0

        result = weighted_sum / total_weight
        return max(-1.0, min(1.0, result))

    def _composite_confidence(self, signals: list[SentimentSignal]) -> float:
        """Calculate confidence of the aggregate.

        Higher when signals agree, lower when they diverge.
        """
        if not signals:
            return 0.0

        confidences = [s.confidence for s in signals]
        scores = [s.score for s in signals]

        mean_confidence = sum(confidences) / len(confidences)

        # Agreement factor: if all signals point same direction, boost confidence
        if len(scores) >= 2:
            score_std = (sum((s - sum(scores) / len(scores)) ** 2 for s in scores) / len(scores)) ** 0.5
            agreement = max(0.0, 1.0 - score_std)
        else:
            agreement = 0.5

        return min(1.0, mean_confidence * (0.6 + 0.4 * agreement))

    def _score_to_label(self, score: float) -> SentimentLabel:
        if score <= -0.6:
            return SentimentLabel.VERY_BEARISH
        elif score <= -0.2:
            return SentimentLabel.BEARISH
        elif score >= 0.6:
            return SentimentLabel.VERY_BULLISH
        elif score >= 0.2:
            return SentimentLabel.BULLISH
        return SentimentLabel.NEUTRAL
