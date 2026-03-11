"""Scenario template loader from YAML configuration."""

from __future__ import annotations

from investorframe.core.config import AppConfig
from investorframe.core.models import ScenarioEvent, ScenarioTemplate
from investorframe.core.types import Direction, EventSubtype, EventType, RegimeState, Severity


class ScenarioTemplateLoader:
    """Parses scenarios.yaml into ScenarioTemplate objects."""

    def __init__(self, config: AppConfig) -> None:
        self.config = config
        self._templates: dict[str, ScenarioTemplate] = {}
        self._load_templates()

    def _load_templates(self) -> None:
        """Parse YAML into template objects."""
        raw = self.config.scenarios.get("scenarios", {})
        for name, data in raw.items():
            events = []
            for ev in data.get("events", []):
                events.append(
                    ScenarioEvent(
                        event_type=EventType(ev["event_type"]),
                        subtype=EventSubtype(ev["subtype"]),
                        severity=Severity(ev["severity"]),
                        direction=Direction(ev["direction"]),
                        headline=ev["headline"],
                        confidence=ev.get("confidence", 0.8),
                    )
                )

            regime_override = None
            if data.get("regime_override"):
                regime_override = RegimeState(data["regime_override"])

            self._templates[name] = ScenarioTemplate(
                name=name,
                description=data.get("description", ""),
                events=events,
                regime_override=regime_override,
            )

    def get_template(self, name: str) -> ScenarioTemplate | None:
        """Get a scenario template by name."""
        return self._templates.get(name)

    def list_scenarios(self) -> list[str]:
        """Return all available scenario names."""
        return list(self._templates.keys())

    def get_all_templates(self) -> dict[str, ScenarioTemplate]:
        """Return all templates."""
        return dict(self._templates)
