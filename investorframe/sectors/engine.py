"""Sector scoring engine — event contributions → normalized scores."""

from __future__ import annotations

import logging
import math
from collections import defaultdict
from datetime import datetime, timezone

from investorframe.core.config import AppConfig
from investorframe.core.models import Event, EventContribution, MarketRegime, SectorScore
from investorframe.core.types import Direction, RegimeState
from investorframe.sectors.mapper import EventSectorMapper

logger = logging.getLogger(__name__)


class SectorScoringEngine:
    """Scores and ranks sectors based on event contributions and regime context."""

    def __init__(self, config: AppConfig) -> None:
        self.config = config
        self.mapper = EventSectorMapper(config)
        self._sector_metadata = config.sector_config.get("sectors", {})
        scoring_params = config.sector_config.get("scoring", {})
        self._scale_factor = scoring_params.get("scale_factor", 10.0)
        self._min_events = scoring_params.get("min_events_for_confidence", 3)
        self._expected_events = scoring_params.get("expected_events_per_sector", 5)

    def score_all(
        self,
        events: list[Event],
        regime: MarketRegime | None = None,
    ) -> list[SectorScore]:
        """Score all configured sectors and return ranked list."""
        # 1. Collect contributions per sector
        sector_contributions: dict[str, list[EventContribution]] = defaultdict(list)
        sector_raw_scores: dict[str, float] = defaultdict(float)

        for event in events:
            mappings = self.mapper.get_mappings(
                event.event_type.value, event.subtype.value
            )
            for mapping in mappings:
                # Determine contribution direction
                direction_sign = self._resolve_direction_sign(
                    event.direction.value, mapping.direction
                )
                contribution = event.effective_severity * mapping.weight * direction_sign

                sector_contributions[mapping.sector].append(
                    EventContribution(
                        event_id=event.id,
                        headline=event.headline,
                        direction=Direction.BULLISH if contribution > 0 else Direction.BEARISH,
                        contribution=round(contribution, 4),
                        weight=mapping.weight,
                    )
                )
                sector_raw_scores[mapping.sector] += contribution

        # 2. Score each sector
        scores: list[SectorScore] = []
        for symbol, meta in self._sector_metadata.items():
            raw_score = sector_raw_scores.get(symbol, 0.0)
            contributions = sector_contributions.get(symbol, [])

            # 3. Apply regime modifier
            regime_mod = self._regime_modifier(raw_score, regime) if regime else 1.0
            modified_score = raw_score * regime_mod

            # 4. Normalize via tanh to [-100, +100]
            normalized = 100.0 * math.tanh(modified_score / self._scale_factor)

            # 5. Calculate confidence
            event_count = len(contributions)
            coverage = min(1.0, event_count / self._expected_events)
            regime_confidence = regime.confidence if regime else 0.5
            confidence = coverage * regime_confidence

            # 6. Determine direction
            direction = self._determine_direction(contributions, normalized)

            # Sort contributions by absolute contribution
            sorted_contribs = sorted(
                contributions, key=lambda c: abs(c.contribution), reverse=True
            )

            scores.append(
                SectorScore(
                    symbol=symbol,
                    name=meta.get("name", symbol),
                    score=round(normalized, 2),
                    direction=direction,
                    confidence=round(min(1.0, confidence), 4),
                    driving_events=sorted_contribs[:10],
                    regime_modifier=round(regime_mod, 4),
                    raw_score=round(raw_score, 4),
                    event_count=event_count,
                )
            )

        # 7. Rank by |score| descending
        scores.sort(key=lambda s: abs(s.score), reverse=True)
        ranked = []
        for i, s in enumerate(scores, 1):
            ranked.append(
                SectorScore(
                    symbol=s.symbol,
                    name=s.name,
                    score=s.score,
                    direction=s.direction,
                    confidence=s.confidence,
                    rank=i,
                    driving_events=s.driving_events,
                    regime_modifier=s.regime_modifier,
                    raw_score=s.raw_score,
                    event_count=s.event_count,
                )
            )

        return ranked

    def _resolve_direction_sign(self, event_direction: str, mapping_direction: str) -> float:
        """Resolve the sign of a contribution.

        If mapping is "neutral", inherit from event.
        If mapping is fixed ("bullish"/"bearish"), use that direction.
        If event opposes the mapping direction, invert.
        """
        if mapping_direction == "neutral":
            if event_direction == "bullish":
                return 1.0
            elif event_direction == "bearish":
                return -1.0
            return 0.0

        mapping_sign = 1.0 if mapping_direction == "bullish" else -1.0

        # If event is bearish and mapping says bullish, invert
        if event_direction == "bearish":
            return -mapping_sign
        return mapping_sign

    def _regime_modifier(self, raw_score: float, regime: MarketRegime | None) -> float:
        """Apply regime-based amplification/dampening."""
        if regime is None:
            return 1.0

        if regime.state == RegimeState.RISK_ON:
            return 1.2 if raw_score > 0 else 0.9
        elif regime.state == RegimeState.RISK_OFF:
            return 0.9 if raw_score > 0 else 1.2
        return 1.0

    def _determine_direction(
        self, contributions: list[EventContribution], normalized_score: float
    ) -> Direction:
        """Determine aggregate direction from contributions and score."""
        if not contributions:
            return Direction.NEUTRAL

        positive = sum(1 for c in contributions if c.contribution > 0)
        negative = sum(1 for c in contributions if c.contribution < 0)
        total = positive + negative

        if total > 0:
            opposing_pct = min(positive, negative) / total
            if opposing_pct >= 0.4:
                return Direction.MIXED

        if normalized_score > 10:
            return Direction.BULLISH
        elif normalized_score < -10:
            return Direction.BEARISH
        return Direction.NEUTRAL
