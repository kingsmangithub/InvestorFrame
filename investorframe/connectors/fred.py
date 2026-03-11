"""FRED API connector for economic indicator data."""

from __future__ import annotations

import logging
from datetime import date, datetime, timedelta, timezone

import httpx

from investorframe.connectors.base import BaseConnector
from investorframe.core.config import AppConfig
from investorframe.core.models import EconomicDataPoint

logger = logging.getLogger(__name__)

FRED_BASE_URL = "https://api.stlouisfed.org/fred/series/observations"


class FredConnector(BaseConnector):
    """Fetches economic indicator data from FRED API."""

    DEFAULT_SERIES: list[str] = [
        "UNRATE",       # unemployment rate
        "CPIAUCSL",     # CPI (inflation)
        "GDP",          # gross domestic product
        "FEDFUNDS",     # federal funds rate
        "T10Y2Y",       # 10Y-2Y treasury spread (yield curve)
        "UMCSENT",      # consumer sentiment
        "INDPRO",       # industrial production
        "RSAFS",        # retail sales
    ]

    SERIES_NAMES: dict[str, str] = {
        "UNRATE": "Unemployment Rate",
        "CPIAUCSL": "Consumer Price Index",
        "GDP": "Gross Domestic Product",
        "FEDFUNDS": "Federal Funds Rate",
        "T10Y2Y": "10Y-2Y Treasury Spread",
        "UMCSENT": "Consumer Sentiment",
        "INDPRO": "Industrial Production",
        "RSAFS": "Retail Sales",
    }

    def __init__(
        self,
        config: AppConfig,
        series_ids: list[str] | None = None,
        lookback_days: int | None = None,
    ) -> None:
        super().__init__(config)
        self.api_key = config.connectors.fred_api_key
        self.series_ids = series_ids or self.DEFAULT_SERIES
        self.lookback_days = lookback_days or config.pipeline.lookback_days

    def fetch(self) -> list[EconomicDataPoint]:
        """Fetch latest values for all configured FRED series."""
        results: list[EconomicDataPoint] = []
        for series_id in self.series_ids:
            point = self.fetch_series(series_id)
            if point is not None:
                results.append(point)
        self._update_timestamp()
        return results

    def fetch_series(self, series_id: str) -> EconomicDataPoint | None:
        """Fetch a single FRED series."""
        if not self.api_key:
            logger.warning("FRED API key not set, skipping %s", series_id)
            return None

        end_date = date.today()
        start_date = end_date - timedelta(days=self.lookback_days + 90)

        params = {
            "series_id": series_id,
            "api_key": self.api_key,
            "file_type": "json",
            "sort_order": "desc",
            "limit": 5,
            "observation_start": start_date.isoformat(),
            "observation_end": end_date.isoformat(),
        }

        try:
            resp = httpx.get(FRED_BASE_URL, params=params, timeout=15.0)
            resp.raise_for_status()
            data = resp.json()
        except Exception as exc:
            logger.error("FRED fetch failed for %s: %s", series_id, exc)
            return None

        observations = data.get("observations", [])
        # Filter out missing values
        observations = [o for o in observations if o.get("value", ".") != "."]
        if not observations:
            return None

        latest = observations[0]
        value = float(latest["value"])

        previous_value = None
        change_pct = None
        if len(observations) >= 2:
            previous_value = float(observations[1]["value"])
            if previous_value != 0:
                change_pct = ((value - previous_value) / abs(previous_value)) * 100

        return EconomicDataPoint(
            series_id=series_id,
            series_name=self.SERIES_NAMES.get(series_id, series_id),
            value=value,
            date=date.fromisoformat(latest["date"]),
            previous_value=previous_value,
            change_pct=round(change_pct, 4) if change_pct is not None else None,
            unit="percent" if series_id in ("UNRATE", "FEDFUNDS", "T10Y2Y") else "index",
        )

    def health_check(self) -> bool:
        """Verify FRED API key is valid and service is reachable."""
        if not self.api_key:
            return False
        try:
            params = {
                "series_id": "UNRATE",
                "api_key": self.api_key,
                "file_type": "json",
                "limit": 1,
            }
            resp = httpx.get(FRED_BASE_URL, params=params, timeout=10.0)
            return resp.status_code == 200
        except Exception:
            return False
