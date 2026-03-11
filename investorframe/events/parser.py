"""Converts raw connector data into structured Event objects."""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from difflib import SequenceMatcher

from investorframe.core.config import AppConfig
from investorframe.core.models import EconomicDataPoint, Event, RawNewsArticle
from investorframe.core.types import (
    DataSource,
    Direction,
    EventSubtype,
    EventType,
    Severity,
)

logger = logging.getLogger(__name__)


class EventParser:
    """Converts raw connector data into structured Event objects."""

    def __init__(self, config: AppConfig) -> None:
        self.config = config
        self._event_type_rules: dict = config.event_types

    def parse_news_articles(self, articles: list[RawNewsArticle]) -> list[Event]:
        """Parse and deduplicate news articles into events."""
        events: list[Event] = []
        for article in articles:
            event = Event(
                event_type=EventType.ECONOMIC,
                subtype=EventSubtype.GDP_REPORT,
                source=DataSource.NEWSAPI,
                timestamp=article.published_at,
                severity=Severity.MODERATE,
                direction=Direction.NEUTRAL,
                confidence=0.5,
                headline=article.title,
                summary=article.description or "",
                raw_text=article.content or article.title,
            )
            events.append(event)
        return self._deduplicate(events)

    def parse_economic_data(self, data_points: list[EconomicDataPoint]) -> list[Event]:
        """Convert significant economic data changes into events."""
        events: list[Event] = []
        for dp in data_points:
            if not self._assess_economic_significance(dp):
                continue

            direction = Direction.NEUTRAL
            if dp.change_pct is not None:
                if dp.change_pct > 0:
                    direction = Direction.BULLISH
                elif dp.change_pct < 0:
                    direction = Direction.BEARISH

            severity = Severity.MODERATE
            if dp.change_pct is not None:
                abs_change = abs(dp.change_pct)
                if abs_change > 2.0:
                    severity = Severity.HIGH
                elif abs_change > 5.0:
                    severity = Severity.CRITICAL

            subtype = self._series_to_subtype(dp.series_id)

            event = Event(
                event_type=EventType.ECONOMIC,
                subtype=subtype,
                source=DataSource.FRED,
                timestamp=datetime.combine(dp.date, datetime.min.time(), tzinfo=timezone.utc),
                severity=severity,
                direction=direction,
                confidence=0.8,
                headline=f"{dp.series_name}: {dp.value:.2f} ({dp.change_pct:+.2f}%)" if dp.change_pct else f"{dp.series_name}: {dp.value:.2f}",
                summary=f"Latest {dp.series_name} reading: {dp.value} {dp.unit}",
                metadata={"series_id": dp.series_id, "value": dp.value},
            )
            events.append(event)

        return events

    def _deduplicate(self, events: list[Event], threshold: float = 0.8) -> list[Event]:
        """Remove near-duplicate events by headline similarity."""
        if not events:
            return events

        unique: list[Event] = [events[0]]
        for event in events[1:]:
            is_dup = False
            for existing in unique:
                ratio = SequenceMatcher(
                    None,
                    event.headline.lower(),
                    existing.headline.lower(),
                ).ratio()
                if ratio >= threshold:
                    is_dup = True
                    break
            if not is_dup:
                unique.append(event)

        logger.info("Deduplicated %d -> %d events", len(events), len(unique))
        return unique

    def _assess_economic_significance(self, dp: EconomicDataPoint) -> bool:
        """Determine if an economic data point warrants an event."""
        if dp.change_pct is None:
            return True  # First observation, always significant

        thresholds = self._event_type_rules.get("event_types", {}).get("economic", {}).get("subtypes", {})

        series_subtype = self._series_to_subtype_name(dp.series_id)
        subtype_config = thresholds.get(series_subtype, {})

        threshold_pct = subtype_config.get("threshold_pct", 0.5)
        return abs(dp.change_pct) >= threshold_pct

    def _series_to_subtype(self, series_id: str) -> EventSubtype:
        """Map FRED series ID to EventSubtype."""
        mapping = {
            "UNRATE": EventSubtype.JOBS_REPORT,
            "CPIAUCSL": EventSubtype.INFLATION_DATA,
            "GDP": EventSubtype.GDP_REPORT,
            "FEDFUNDS": EventSubtype.RATE_DECISION,
            "T10Y2Y": EventSubtype.RATE_DECISION,
            "UMCSENT": EventSubtype.CONSUMER_CONFIDENCE,
            "INDPRO": EventSubtype.PMI,
            "RSAFS": EventSubtype.RETAIL_SALES,
        }
        return mapping.get(series_id, EventSubtype.GDP_REPORT)

    def _series_to_subtype_name(self, series_id: str) -> str:
        """Map FRED series ID to subtype config name."""
        mapping = {
            "UNRATE": "jobs_report",
            "CPIAUCSL": "inflation_data",
            "GDP": "gdp_report",
            "FEDFUNDS": "rate_decision",
            "T10Y2Y": "rate_decision",
            "UMCSENT": "consumer_confidence",
            "INDPRO": "pmi",
            "RSAFS": "retail_sales",
        }
        return mapping.get(series_id, "gdp_report")
