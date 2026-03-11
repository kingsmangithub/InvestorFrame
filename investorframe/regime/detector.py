"""Market regime detection via indicator voting system."""

from __future__ import annotations

import logging
from datetime import datetime, timezone

from investorframe.core.config import AppConfig
from investorframe.core.models import EconomicDataPoint, MarketRegime, MarketSnapshot
from investorframe.core.types import RegimeState
from investorframe.regime.indicators import IndicatorCalculator

logger = logging.getLogger(__name__)


class RegimeDetector:
    """Determines the current market regime from indicator thresholds."""

    def __init__(self, config: AppConfig) -> None:
        self.config = config
        self.rules = config.regime_rules
        self.calculator = IndicatorCalculator()

    def detect(
        self,
        snapshots: list[MarketSnapshot],
        economic_data: list[EconomicDataPoint],
    ) -> MarketRegime:
        """Run all indicators through regime_rules.yaml thresholds."""
        indicator_values: dict[str, float] = {}
        votes: dict[str, float] = {}  # state -> total weighted votes
        factors: list[str] = []

        # Calculate indicators
        vix = self.calculator.vix_level(snapshots)
        if vix is not None:
            indicator_values["vix"] = vix
            self._vote_vix(vix, votes, factors)

        spread = self.calculator.yield_curve_spread(economic_data)
        if spread is not None:
            indicator_values["yield_curve"] = spread
            self._vote_yield_curve(spread, votes, factors)

        breadth = self.calculator.market_breadth(snapshots)
        if breadth is not None:
            indicator_values["market_breadth"] = breadth
            self._vote_breadth(breadth, votes, factors)

        trend = self.calculator.trend_strength(snapshots)
        if trend is not None:
            indicator_values["trend_strength"] = trend
            self._vote_trend(trend, votes, factors)

        cs_zscore = self.calculator.consumer_sentiment_zscore(economic_data)
        if cs_zscore is not None:
            indicator_values["consumer_sentiment_zscore"] = cs_zscore
            self._vote_consumer_sentiment(cs_zscore, votes, factors)

        # Determine winning regime
        state, confidence = self._resolve_votes(votes)

        return MarketRegime(
            state=state,
            confidence=round(confidence, 4),
            contributing_factors=factors,
            indicator_values=indicator_values,
        )

    def _vote_vix(self, vix: float, votes: dict[str, float], factors: list[str]) -> None:
        thresholds = self.rules.get("indicators", {}).get("vix", {}).get("thresholds", {})

        if vix < thresholds.get("risk_on", {}).get("below", 16.0):
            weight = thresholds.get("risk_on", {}).get("weight", 0.25)
            votes["risk_on"] = votes.get("risk_on", 0) + weight
            factors.append(f"VIX={vix:.1f} (low, risk-on)")
        elif vix > thresholds.get("risk_off", {}).get("above", 28.0):
            weight = thresholds.get("risk_off", {}).get("weight", 0.30)
            votes["risk_off"] = votes.get("risk_off", 0) + weight
            factors.append(f"VIX={vix:.1f} (elevated, risk-off)")
        else:
            weight = thresholds.get("uncertainty", {}).get("weight", 0.20)
            votes["uncertainty"] = votes.get("uncertainty", 0) + weight
            factors.append(f"VIX={vix:.1f} (moderate)")

    def _vote_yield_curve(self, spread: float, votes: dict[str, float], factors: list[str]) -> None:
        thresholds = self.rules.get("indicators", {}).get("yield_curve", {}).get("thresholds", {})

        if spread > thresholds.get("risk_on", {}).get("above", 0.5):
            weight = thresholds.get("risk_on", {}).get("weight", 0.20)
            votes["risk_on"] = votes.get("risk_on", 0) + weight
            factors.append(f"Yield curve={spread:.2f}% (normal, risk-on)")
        elif spread < thresholds.get("risk_off", {}).get("below", -0.2):
            weight = thresholds.get("risk_off", {}).get("weight", 0.25)
            votes["risk_off"] = votes.get("risk_off", 0) + weight
            factors.append(f"Yield curve={spread:.2f}% (inverted, risk-off)")
        else:
            weight = thresholds.get("uncertainty", {}).get("weight", 0.15)
            votes["uncertainty"] = votes.get("uncertainty", 0) + weight
            factors.append(f"Yield curve={spread:.2f}% (flat)")

    def _vote_breadth(self, breadth: float, votes: dict[str, float], factors: list[str]) -> None:
        thresholds = self.rules.get("indicators", {}).get("market_breadth", {}).get("thresholds", {})

        if breadth > thresholds.get("risk_on", {}).get("above", 0.65):
            weight = thresholds.get("risk_on", {}).get("weight", 0.20)
            votes["risk_on"] = votes.get("risk_on", 0) + weight
            factors.append(f"Breadth={breadth:.0%} above 50MA (strong)")
        elif breadth < thresholds.get("risk_off", {}).get("below", 0.35):
            weight = thresholds.get("risk_off", {}).get("weight", 0.25)
            votes["risk_off"] = votes.get("risk_off", 0) + weight
            factors.append(f"Breadth={breadth:.0%} above 50MA (weak)")
        else:
            weight = thresholds.get("uncertainty", {}).get("weight", 0.15)
            votes["uncertainty"] = votes.get("uncertainty", 0) + weight
            factors.append(f"Breadth={breadth:.0%} above 50MA (mixed)")

    def _vote_trend(self, trend: float, votes: dict[str, float], factors: list[str]) -> None:
        thresholds = self.rules.get("indicators", {}).get("trend_strength", {}).get("thresholds", {})

        if trend > thresholds.get("risk_on", {}).get("above", 3.0):
            weight = thresholds.get("risk_on", {}).get("weight", 0.15)
            votes["risk_on"] = votes.get("risk_on", 0) + weight
            factors.append(f"Trend={trend:+.1f}% from 200MA (bullish)")
        elif trend < thresholds.get("risk_off", {}).get("below", -5.0):
            weight = thresholds.get("risk_off", {}).get("weight", 0.20)
            votes["risk_off"] = votes.get("risk_off", 0) + weight
            factors.append(f"Trend={trend:+.1f}% from 200MA (bearish)")
        else:
            weight = thresholds.get("uncertainty", {}).get("weight", 0.10)
            votes["uncertainty"] = votes.get("uncertainty", 0) + weight
            factors.append(f"Trend={trend:+.1f}% from 200MA (neutral)")

    def _vote_consumer_sentiment(self, zscore: float, votes: dict[str, float], factors: list[str]) -> None:
        thresholds = self.rules.get("indicators", {}).get("consumer_sentiment", {}).get("thresholds", {})

        if zscore > thresholds.get("risk_on", {}).get("zscore_above", 0.5):
            weight = thresholds.get("risk_on", {}).get("weight", 0.10)
            votes["risk_on"] = votes.get("risk_on", 0) + weight
            factors.append(f"Consumer sentiment z={zscore:+.2f} (optimistic)")
        elif zscore < thresholds.get("risk_off", {}).get("zscore_below", -1.0):
            weight = thresholds.get("risk_off", {}).get("weight", 0.15)
            votes["risk_off"] = votes.get("risk_off", 0) + weight
            factors.append(f"Consumer sentiment z={zscore:+.2f} (pessimistic)")
        else:
            weight = thresholds.get("uncertainty", {}).get("weight", 0.10)
            votes["uncertainty"] = votes.get("uncertainty", 0) + weight
            factors.append(f"Consumer sentiment z={zscore:+.2f} (moderate)")

    def _resolve_votes(self, votes: dict[str, float]) -> tuple[RegimeState, float]:
        """Resolve votes into a regime state and confidence."""
        decision = self.rules.get("decision", {})
        transition_threshold = decision.get("transition_threshold", 0.45)
        ambiguity_margin = decision.get("ambiguity_margin", 0.10)

        if not votes:
            return RegimeState.UNCERTAINTY, 0.0

        sorted_states = sorted(votes.items(), key=lambda x: x[1], reverse=True)
        top_state, top_votes = sorted_states[0]

        # Check ambiguity
        if len(sorted_states) >= 2:
            second_votes = sorted_states[1][1]
            if top_votes - second_votes < ambiguity_margin:
                return RegimeState.UNCERTAINTY, round(top_votes, 4)

        # Check transition threshold
        if top_votes < transition_threshold:
            return RegimeState.TRANSITION, round(top_votes, 4)

        state_map = {
            "risk_on": RegimeState.RISK_ON,
            "risk_off": RegimeState.RISK_OFF,
            "uncertainty": RegimeState.UNCERTAINTY,
        }

        return state_map.get(top_state, RegimeState.UNCERTAINTY), round(top_votes, 4)
