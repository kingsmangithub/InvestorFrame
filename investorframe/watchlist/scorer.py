"""Stock scoring with sector inheritance and beta amplification."""

from __future__ import annotations

import logging
from datetime import datetime, timezone

from investorframe.core.config import AppConfig
from investorframe.core.models import EventContribution, SectorScore, StockScore
from investorframe.core.types import Direction, SignalLabel

logger = logging.getLogger(__name__)


class StockScorer:
    """Scores individual watchlist stocks based on sector dynamics."""

    def __init__(self, config: AppConfig) -> None:
        self.config = config
        watchlist_config = config.watchlist
        self._stocks = watchlist_config.get("stocks", {})
        scoring = watchlist_config.get("scoring", {})
        self._sector_weight = scoring.get("sector_inheritance_weight", 0.70)
        self._beta_amplification = scoring.get("beta_amplification", True)
        self._beta_cap = scoring.get("beta_dampening_cap", 2.0)

    def score_stock(
        self,
        symbol: str,
        sector_scores: list[SectorScore],
    ) -> StockScore | None:
        """Score a single stock based on its sector score."""
        stock_config = self._stocks.get(symbol)
        if stock_config is None:
            return None

        sector_symbol = stock_config["sector"]
        sector_score = next(
            (s for s in sector_scores if s.symbol == sector_symbol), None
        )
        if sector_score is None:
            return None

        # Sector inheritance
        inherited = sector_score.score * self._sector_weight
        beta = min(stock_config.get("beta", 1.0), self._beta_cap)

        # Apply beta amplification
        if self._beta_amplification:
            amplified = inherited * beta
        else:
            amplified = inherited

        # Decompose into tailwind/headwind
        if amplified >= 0:
            tailwind = min(100.0, abs(amplified))
            headwind = 0.0
        else:
            tailwind = 0.0
            headwind = min(100.0, abs(amplified))

        net_signal = max(-100.0, min(100.0, amplified))
        label = self._assign_label(net_signal)

        # Build explanation
        explanation = self._build_explanation(
            symbol, stock_config, sector_score, net_signal, label
        )

        return StockScore(
            symbol=symbol,
            name=stock_config["name"],
            sector=sector_symbol,
            sector_name=sector_score.name,
            tailwind_score=round(tailwind, 2),
            headwind_score=round(headwind, 2),
            net_signal=round(net_signal, 2),
            label=label,
            confidence=sector_score.confidence,
            explanation=explanation,
            driving_events=sector_score.driving_events[:5],
            sector_score_contribution=round(inherited, 2),
        )

    def score_all(self, sector_scores: list[SectorScore]) -> list[StockScore]:
        """Score all watchlist stocks."""
        scores: list[StockScore] = []
        for symbol in self._stocks:
            stock_score = self.score_stock(symbol, sector_scores)
            if stock_score is not None:
                scores.append(stock_score)

        # Rank by |net_signal|
        scores.sort(key=lambda s: abs(s.net_signal), reverse=True)
        ranked = []
        for i, s in enumerate(scores, 1):
            ranked.append(
                StockScore(
                    symbol=s.symbol,
                    name=s.name,
                    sector=s.sector,
                    sector_name=s.sector_name,
                    tailwind_score=s.tailwind_score,
                    headwind_score=s.headwind_score,
                    net_signal=s.net_signal,
                    label=s.label,
                    confidence=s.confidence,
                    explanation=s.explanation,
                    driving_events=s.driving_events,
                    sector_score_contribution=s.sector_score_contribution,
                    rank=i,
                )
            )
        return ranked

    def _assign_label(self, net_signal: float) -> SignalLabel:
        """Assign signal label based on net signal value."""
        if net_signal > 40:
            return SignalLabel.STRONG_TAILWIND
        elif net_signal > 15:
            return SignalLabel.TAILWIND
        elif net_signal < -40:
            return SignalLabel.STRONG_HEADWIND
        elif net_signal < -15:
            return SignalLabel.HEADWIND
        elif abs(net_signal) <= 5:
            return SignalLabel.NEUTRAL
        return SignalLabel.MIXED

    def _build_explanation(
        self,
        symbol: str,
        stock_config: dict,
        sector_score: SectorScore,
        net_signal: float,
        label: SignalLabel,
    ) -> str:
        """Generate a human-readable scoring explanation."""
        beta = stock_config.get("beta", 1.0)
        parts = [
            f"{symbol} ({stock_config['name']}) shows {label.value} signal ({net_signal:+.1f}).",
            f"Primary driver: {sector_score.name} sector score of {sector_score.score:+.1f} "
            f"({sector_score.direction.value}).",
        ]
        if beta != 1.0:
            parts.append(f"Beta of {beta:.2f} {'amplifies' if beta > 1 else 'dampens'} sector exposure.")

        top_events = sector_score.driving_events[:3]
        if top_events:
            event_summaries = ", ".join(e.headline[:60] for e in top_events)
            parts.append(f"Key events: {event_summaries}.")

        return " ".join(parts)
