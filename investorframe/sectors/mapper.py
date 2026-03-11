"""Event-to-sector mapping via YAML rules."""

from __future__ import annotations

import logging
from dataclasses import dataclass

from investorframe.core.config import AppConfig

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class SectorMapping:
    """A single mapping from an event subtype to a sector."""

    sector: str
    direction: str  # "bullish" | "bearish" | "neutral"
    weight: float
    decay_days: int


class EventSectorMapper:
    """Loads event_sector_map.yaml and resolves event→sector mappings."""

    def __init__(self, config: AppConfig) -> None:
        self.config = config
        self._mappings: dict[str, dict[str, list[SectorMapping]]] = {}
        self._load_mappings()

    def _load_mappings(self) -> None:
        """Parse event_sector_map.yaml into SectorMapping lookup structure."""
        raw = self.config.event_sector_map.get("mappings", {})

        for event_type, subtypes in raw.items():
            self._mappings[event_type] = {}
            for subtype, entries in subtypes.items():
                self._mappings[event_type][subtype] = [
                    SectorMapping(
                        sector=entry["sector"],
                        direction=entry.get("direction", "neutral"),
                        weight=entry.get("weight", 0.5),
                        decay_days=entry.get("decay_days", 7),
                    )
                    for entry in entries
                ]

    def get_mappings(self, event_type: str, subtype: str) -> list[SectorMapping]:
        """Look up sector mappings for an event type/subtype pair."""
        type_mappings = self._mappings.get(event_type, {})
        return type_mappings.get(subtype, [])

    def get_all_affected_sectors(self, event_type: str, subtype: str) -> list[str]:
        """Return list of sector symbols affected by an event."""
        return [m.sector for m in self.get_mappings(event_type, subtype)]
