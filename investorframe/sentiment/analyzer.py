"""Multi-source sentiment analysis."""

from __future__ import annotations

import logging
from datetime import datetime, timezone

from investorframe.core.config import AppConfig
from investorframe.core.models import Event, MarketSnapshot, RawNewsArticle, SentimentSignal
from investorframe.core.types import DataSource, SentimentLabel

logger = logging.getLogger(__name__)


class SentimentAnalyzer:
    """Produces sentiment signals from various data sources."""

    BULLISH_KEYWORDS: set[str] = {
        "surge", "rally", "gain", "beat", "growth", "recovery",
        "optimism", "expansion", "upgrade", "bullish",
    }
    BEARISH_KEYWORDS: set[str] = {
        "crash", "plunge", "loss", "miss", "recession", "decline",
        "fear", "downgrade", "bearish", "contraction",
    }

    def __init__(
        self,
        config: AppConfig,
        llm: object | None = None,
    ) -> None:
        self.config = config
        self.llm = llm

    def analyze_events(self, events: list[Event]) -> SentimentSignal:
        """Derive sentiment from classified events."""
        if not events:
            return SentimentSignal(
                source=DataSource.MANUAL,
                score=0.0,
                label=SentimentLabel.NEUTRAL,
                confidence=0.0,
                sample_size=0,
            )

        total_weight = 0.0
        weighted_score = 0.0

        for event in events:
            weight = event.effective_severity
            if event.direction.value == "bullish":
                score = 1.0
            elif event.direction.value == "bearish":
                score = -1.0
            else:
                score = 0.0

            weighted_score += score * weight
            total_weight += weight

        composite = weighted_score / total_weight if total_weight > 0 else 0.0
        composite = max(-1.0, min(1.0, composite))
        confidence = min(1.0, len(events) / 10.0) * 0.8

        return SentimentSignal(
            source=DataSource.FRED,
            score=round(composite, 4),
            label=self._score_to_label(composite),
            confidence=round(confidence, 4),
            sample_size=len(events),
        )

    def analyze_news(self, articles: list[RawNewsArticle]) -> SentimentSignal:
        """Derive sentiment from raw news article text."""
        if not articles:
            return SentimentSignal(
                source=DataSource.NEWSAPI,
                score=0.0,
                label=SentimentLabel.NEUTRAL,
                confidence=0.0,
                sample_size=0,
            )

        scores: list[float] = []
        for article in articles:
            text = f"{article.title} {article.description or ''}".lower()
            bull = sum(1 for kw in self.BULLISH_KEYWORDS if kw in text)
            bear = sum(1 for kw in self.BEARISH_KEYWORDS if kw in text)

            total = bull + bear
            if total > 0:
                score = (bull - bear) / total
            else:
                score = 0.0
            scores.append(score)

        avg_score = sum(scores) / len(scores) if scores else 0.0
        avg_score = max(-1.0, min(1.0, avg_score))
        confidence = min(1.0, len(articles) / 20.0) * 0.7

        return SentimentSignal(
            source=DataSource.NEWSAPI,
            score=round(avg_score, 4),
            label=self._score_to_label(avg_score),
            confidence=round(confidence, 4),
            sample_size=len(articles),
        )

    def analyze_market_data(self, snapshots: list[MarketSnapshot]) -> SentimentSignal:
        """Derive sentiment from market price action and VIX."""
        if not snapshots:
            return SentimentSignal(
                source=DataSource.YFINANCE,
                score=0.0,
                label=SentimentLabel.NEUTRAL,
                confidence=0.0,
                sample_size=0,
            )

        scores: list[float] = []
        for snap in snapshots:
            # VIX-based sentiment
            if snap.vix is not None:
                if snap.vix > 30:
                    scores.append(-0.8)
                elif snap.vix > 20:
                    scores.append(-0.3)
                elif snap.vix < 15:
                    scores.append(0.5)
                else:
                    scores.append(0.0)
            else:
                # Price-based sentiment
                if snap.change_pct > 1.0:
                    scores.append(0.6)
                elif snap.change_pct > 0.3:
                    scores.append(0.3)
                elif snap.change_pct < -1.0:
                    scores.append(-0.6)
                elif snap.change_pct < -0.3:
                    scores.append(-0.3)
                else:
                    scores.append(0.0)

        avg_score = sum(scores) / len(scores) if scores else 0.0
        avg_score = max(-1.0, min(1.0, avg_score))

        return SentimentSignal(
            source=DataSource.YFINANCE,
            score=round(avg_score, 4),
            label=self._score_to_label(avg_score),
            confidence=0.7,
            sample_size=len(snapshots),
        )

    def _score_to_label(self, score: float) -> SentimentLabel:
        """Convert a -1.0 to +1.0 score to a SentimentLabel."""
        if score <= -0.6:
            return SentimentLabel.VERY_BEARISH
        elif score <= -0.2:
            return SentimentLabel.BEARISH
        elif score >= 0.6:
            return SentimentLabel.VERY_BULLISH
        elif score >= 0.2:
            return SentimentLabel.BULLISH
        return SentimentLabel.NEUTRAL
