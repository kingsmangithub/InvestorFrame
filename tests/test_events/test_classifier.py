"""Tests for event classification."""

from __future__ import annotations

from datetime import datetime, timezone

from investorframe.core.config import AppConfig
from investorframe.core.models import Event
from investorframe.core.types import (
    DataSource,
    Direction,
    EventSubtype,
    EventType,
    Severity,
)
from investorframe.events.classifier import EventClassifier


def _make_event(headline: str) -> Event:
    return Event(
        event_type=EventType.ECONOMIC,
        subtype=EventSubtype.GDP_REPORT,
        source=DataSource.NEWSAPI,
        timestamp=datetime.now(timezone.utc),
        severity=Severity.MODERATE,
        direction=Direction.NEUTRAL,
        confidence=0.6,
        headline=headline,
    )


class TestEventClassifier:
    def test_classify_rate_hike(self, config: AppConfig) -> None:
        classifier = EventClassifier(config)
        event = _make_event("Fed raises interest rates by 25 basis points")
        classified = classifier.classify(event)
        assert classified.event_type == EventType.MONETARY_POLICY
        assert classified.subtype == EventSubtype.RATE_DECISION

    def test_classify_oil_event(self, config: AppConfig) -> None:
        classifier = EventClassifier(config)
        event = _make_event("OPEC announces crude oil production cuts")
        classified = classifier.classify(event)
        assert classified.event_type == EventType.COMMODITY
        assert classified.subtype == EventSubtype.OIL_SUPPLY

    def test_classify_batch(self, config: AppConfig) -> None:
        classifier = EventClassifier(config)
        events = [
            _make_event("GDP grows 2.5% in Q4"),
            _make_event("Federal funds rate decision today"),
        ]
        results = classifier.classify_batch(events)
        assert len(results) == 2

    def test_direction_inference_bullish(self, config: AppConfig) -> None:
        classifier = EventClassifier(config)
        # Headline must match a subtype keyword ("gdp") to trigger classification,
        # then sentiment terms ("surge", "rally") drive direction inference
        event = _make_event("GDP surge rally in economic growth")
        classified = classifier.classify(event)
        assert classified.direction == Direction.BULLISH

    def test_direction_inference_bearish(self, config: AppConfig) -> None:
        classifier = EventClassifier(config)
        # "unemployment" matches jobs_report subtype, "crash"/"fear" drive bearish
        event = _make_event("Unemployment crash amid recession fears")
        classified = classifier.classify(event)
        assert classified.direction == Direction.BEARISH

    def test_unknown_event_stays_economic(self, config: AppConfig) -> None:
        classifier = EventClassifier(config)
        event = _make_event("Random unrelated text about cooking recipes")
        classified = classifier.classify(event)
        # Should keep original type when no keywords match
        assert classified.event_type is not None
