"""Market indicator calculations for regime detection."""

from __future__ import annotations

from investorframe.core.models import EconomicDataPoint, MarketSnapshot


class IndicatorCalculator:
    """Computes derived market indicators from raw data."""

    def vix_level(self, snapshots: list[MarketSnapshot]) -> float | None:
        """Extract current VIX level."""
        for snap in snapshots:
            if snap.vix is not None:
                return snap.vix
            if snap.symbol == "^VIX":
                return snap.price
        return None

    def yield_curve_spread(
        self, data_points: list[EconomicDataPoint]
    ) -> float | None:
        """Extract 10Y-2Y treasury spread from FRED data."""
        for dp in data_points:
            if dp.series_id == "T10Y2Y":
                return dp.value
        return None

    def market_breadth(self, snapshots: list[MarketSnapshot]) -> float | None:
        """Percentage of tracked symbols above their 50-day MA.

        Returns 0.0 (none above) to 1.0 (all above).
        """
        eligible = [s for s in snapshots if s.fifty_day_ma is not None and not s.symbol.startswith("^")]
        if not eligible:
            return None

        above = sum(1 for s in eligible if s.price > s.fifty_day_ma)
        return round(above / len(eligible), 4)

    def trend_strength(self, snapshots: list[MarketSnapshot]) -> float | None:
        """Average % distance of price from 200-day MA for major indices."""
        indices = [s for s in snapshots if s.two_hundred_day_ma is not None and s.symbol.startswith("^")]
        if not indices:
            return None

        distances = []
        for s in indices:
            pct_distance = ((s.price - s.two_hundred_day_ma) / s.two_hundred_day_ma) * 100
            distances.append(pct_distance)

        return round(sum(distances) / len(distances), 4)

    def consumer_sentiment_zscore(
        self, data_points: list[EconomicDataPoint]
    ) -> float | None:
        """Calculate z-score of consumer sentiment relative to historical mean.

        Uses a rough historical baseline of mean=80, std=15 for UMCSENT.
        """
        for dp in data_points:
            if dp.series_id == "UMCSENT":
                historical_mean = 80.0
                historical_std = 15.0
                return round((dp.value - historical_mean) / historical_std, 4)
        return None
