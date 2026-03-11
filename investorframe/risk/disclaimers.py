"""Disclaimer generation for pipeline outputs."""

from __future__ import annotations

from investorframe.core.models import MarketRegime, RiskFlag
from investorframe.core.types import RegimeState, Severity

STANDARD_DISCLAIMER = (
    "This analysis is for informational and educational purposes only. "
    "It does not constitute investment advice, a recommendation to buy or "
    "sell any security, or an offer of any financial product. Past performance "
    "does not guarantee future results. The outputs are probabilistic estimates "
    "based on simplified models and may be inaccurate. Always consult a "
    "qualified financial advisor before making investment decisions."
)


class DisclaimerGenerator:
    """Generates standard and contextual disclaimers."""

    def generate(
        self,
        flags: list[RiskFlag],
        regime: MarketRegime | None = None,
    ) -> list[str]:
        """Generate all applicable disclaimers."""
        disclaimers = [STANDARD_DISCLAIMER]

        # Add risk-flag-specific disclaimers
        for flag in flags:
            if flag.code == "STALE_EVENTS":
                disclaimers.append(
                    "WARNING: Some data sources may be outdated. "
                    "Scores may not reflect the most recent market conditions."
                )
            elif flag.code == "LOW_EVENT_COVERAGE":
                disclaimers.append(
                    "NOTE: Limited event data was available for this analysis. "
                    "Scores have lower confidence due to insufficient data coverage."
                )
            elif flag.code == "UNSTABLE_REGIME":
                disclaimers.append(
                    "CAUTION: The market regime is in transition with low confidence. "
                    "Sector and stock scores may shift significantly in the near term."
                )
            elif flag.code == "CONNECTOR_FAILURE":
                disclaimers.append(
                    "WARNING: One or more data connectors failed. "
                    "This analysis may be based on incomplete data."
                )
            elif flag.code == "EXTREME_SCORE":
                disclaimers.append(
                    "NOTE: Some scores are at extreme levels, which may indicate "
                    "unusual market conditions or model edge cases. Exercise additional caution."
                )

        # Regime-specific disclaimers
        if regime:
            if regime.state == RegimeState.RISK_OFF:
                disclaimers.append(
                    "MARKET CONTEXT: Current indicators suggest a risk-off environment. "
                    "Defensive positioning may be warranted."
                )
            elif regime.state == RegimeState.TRANSITION:
                disclaimers.append(
                    "MARKET CONTEXT: The market regime is in transition. "
                    "Historical patterns may be less reliable during regime changes."
                )

        # Deduplicate
        return list(dict.fromkeys(disclaimers))
