"""Event type/subtype classification using keyword rules and optional LLM."""

from __future__ import annotations

import logging
import re
from typing import Optional, Tuple

from investorframe.core.config import AppConfig
from investorframe.core.models import Event
from investorframe.core.types import Direction, EventSubtype, EventType, Severity

logger = logging.getLogger(__name__)


class EventClassifier:
    """Assigns type, subtype, direction, and severity to events."""

    def __init__(
        self,
        config: AppConfig,
        llm: object | None = None,
    ) -> None:
        self.config = config
        self.llm = llm
        self._keyword_rules = config.event_types.get("event_types", {})
        self._classification_settings = config.event_types.get("classification", {})

    def classify(self, event: Event) -> Event:
        """Classify a single event. Keyword rules first, LLM fallback."""
        text = f"{event.headline} {event.summary} {event.raw_text}".lower()

        result = self._keyword_classify(text)

        if result is not None:
            event_type, subtype, direction, severity = result
            # Create new frozen Event with classified fields
            return Event(
                id=event.id,
                event_type=event_type,
                subtype=subtype,
                source=event.source,
                timestamp=event.timestamp,
                severity=severity,
                direction=direction,
                confidence=max(event.confidence, 0.7),
                headline=event.headline,
                summary=event.summary,
                raw_text=event.raw_text,
                metadata=event.metadata,
                ttl_days=event.ttl_days,
            )

        # LLM fallback
        if self.llm is not None and hasattr(self.llm, "classify_headline"):
            return self._llm_classify(event)

        return event

    def classify_batch(self, events: list[Event]) -> list[Event]:
        """Classify a batch of events."""
        return [self.classify(e) for e in events]

    def _keyword_classify(
        self, text: str
    ) -> Optional[Tuple[EventType, EventSubtype, Direction, Severity]]:
        """Attempt rule-based classification using keyword matching."""
        min_matches = self._classification_settings.get("min_keyword_matches", 1)
        default_severity = self._classification_settings.get("default_severity", 3)

        best_match: Optional[Tuple[EventType, EventSubtype, Direction, Severity]] = None
        best_score = 0

        for type_name, type_config in self._keyword_rules.items():
            try:
                event_type = EventType(type_name)
            except ValueError:
                continue

            subtypes = type_config.get("subtypes", {})
            for subtype_name, subtype_config in subtypes.items():
                try:
                    subtype = EventSubtype(subtype_name)
                except ValueError:
                    continue

                keywords = subtype_config.get("keywords", [])
                match_count = sum(1 for kw in keywords if kw.lower() in text)

                if match_count >= min_matches and match_count > best_score:
                    # Determine direction
                    default_dir = subtype_config.get("default_direction", None)
                    direction = Direction(default_dir) if default_dir else self._infer_direction(text)

                    # Determine severity
                    severity_val = subtype_config.get("default_severity", default_severity)
                    severity_boost = subtype_config.get("severity_boost", 0)
                    severity_val = min(severity_val + severity_boost, 5)
                    severity = Severity(severity_val)

                    best_match = (event_type, subtype, direction, severity)
                    best_score = match_count

        return best_match

    def _infer_direction(self, text: str) -> Direction:
        """Infer direction from sentiment keywords in text."""
        bullish_terms = {"surge", "rally", "gain", "beat", "growth", "recovery",
                         "optimism", "expansion", "upgrade", "bullish", "rise", "jump"}
        bearish_terms = {"crash", "plunge", "loss", "miss", "recession", "decline",
                         "fear", "downgrade", "bearish", "contraction", "fall", "drop"}

        bull_count = sum(1 for term in bullish_terms if term in text)
        bear_count = sum(1 for term in bearish_terms if term in text)

        if bull_count > bear_count:
            return Direction.BULLISH
        elif bear_count > bull_count:
            return Direction.BEARISH
        elif bull_count > 0 and bear_count > 0:
            return Direction.MIXED
        return Direction.NEUTRAL

    def _llm_classify(self, event: Event) -> Event:
        """Use LLM connector for classification."""
        result = self.llm.classify_headline(event.headline, event.summary)  # type: ignore
        if not result:
            return event

        try:
            return Event(
                id=event.id,
                event_type=EventType(result.get("event_type", event.event_type.value)),
                subtype=EventSubtype(result.get("subtype", event.subtype.value)),
                source=event.source,
                timestamp=event.timestamp,
                severity=Severity(int(result.get("severity", event.severity.value))),
                direction=Direction(result.get("direction", event.direction.value)),
                confidence=float(result.get("confidence", event.confidence)),
                headline=event.headline,
                summary=event.summary,
                raw_text=event.raw_text,
                metadata=event.metadata,
                ttl_days=event.ttl_days,
            )
        except (ValueError, KeyError) as exc:
            logger.warning("LLM classification result invalid: %s", exc)
            return event
