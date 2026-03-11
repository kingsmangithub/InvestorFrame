"""Market data connector using yfinance."""

from __future__ import annotations

import logging
from datetime import datetime, timezone

from investorframe.connectors.base import BaseConnector
from investorframe.core.config import AppConfig
from investorframe.core.models import MarketSnapshot

logger = logging.getLogger(__name__)


class MarketConnector(BaseConnector):
    """Fetches market data via yfinance."""

    INDEX_SYMBOLS: list[str] = ["^GSPC", "^VIX", "^DJI", "^IXIC"]

    def __init__(
        self,
        config: AppConfig,
        additional_symbols: list[str] | None = None,
    ) -> None:
        super().__init__(config)
        self.symbols = self.INDEX_SYMBOLS + (additional_symbols or [])

    def fetch(self) -> list[MarketSnapshot]:
        """Fetch current market data for all configured symbols."""
        results: list[MarketSnapshot] = []
        for symbol in self.symbols:
            snap = self.fetch_symbol(symbol)
            if snap is not None:
                results.append(snap)
        self._update_timestamp()
        return results

    def fetch_symbol(self, symbol: str) -> MarketSnapshot | None:
        """Fetch data for a single symbol."""
        try:
            import yfinance as yf
        except ImportError:
            logger.error("yfinance not installed")
            return None

        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="5d")

            if hist.empty:
                logger.warning("No data for %s", symbol)
                return None

            latest = hist.iloc[-1]
            prev_close = hist.iloc[-2]["Close"] if len(hist) >= 2 else latest["Close"]
            change_pct = ((latest["Close"] - prev_close) / prev_close) * 100

            # Get moving averages from longer history
            hist_long = ticker.history(period="1y")
            fifty_day_ma = None
            two_hundred_day_ma = None
            if len(hist_long) >= 50:
                fifty_day_ma = float(hist_long["Close"].tail(50).mean())
            if len(hist_long) >= 200:
                two_hundred_day_ma = float(hist_long["Close"].tail(200).mean())

            vix_value = None
            if symbol == "^VIX":
                vix_value = float(latest["Close"])

            return MarketSnapshot(
                symbol=symbol,
                price=float(latest["Close"]),
                change_pct=round(change_pct, 4),
                volume=int(latest["Volume"]),
                fifty_day_ma=fifty_day_ma,
                two_hundred_day_ma=two_hundred_day_ma,
                vix=vix_value,
                timestamp=datetime.now(timezone.utc),
            )
        except Exception as exc:
            logger.error("yfinance fetch failed for %s: %s", symbol, exc)
            return None

    def get_vix(self) -> float | None:
        """Convenience: fetch current VIX value."""
        snap = self.fetch_symbol("^VIX")
        return snap.price if snap else None

    def get_sector_etf_prices(
        self, sector_symbols: list[str]
    ) -> dict[str, MarketSnapshot]:
        """Fetch current prices for sector ETFs."""
        results: dict[str, MarketSnapshot] = {}
        for symbol in sector_symbols:
            snap = self.fetch_symbol(symbol)
            if snap is not None:
                results[symbol] = snap
        return results

    def health_check(self) -> bool:
        """Verify yfinance can fetch data."""
        try:
            snap = self.fetch_symbol("^GSPC")
            return snap is not None
        except Exception:
            return False
