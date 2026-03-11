"""Application configuration for InvestorFrame.

Aggregates environment variables (via pydantic-settings) and YAML rule
files into a single ``AppConfig`` instance used throughout the pipeline.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from pydantic_settings import BaseSettings


class ConnectorSettings(BaseSettings):
    """API keys and connector-level settings from environment."""

    fred_api_key: str = ""
    newsapi_key: str = ""
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"

    model_config = {"env_prefix": "INVESTORFRAME_"}


class PipelineSettings(BaseSettings):
    """Pipeline tuning parameters from environment."""

    lookback_days: int = 7
    max_events: int = 100
    confidence_floor: float = 0.3
    score_normalization: str = "tanh"
    enable_llm: bool = False
    cache_ttl_minutes: int = 60
    db_url: str = "sqlite:///investorframe.db"

    model_config = {"env_prefix": "INVESTORFRAME_"}


class AppConfig:
    """Central configuration aggregating env vars and YAML rule files."""

    def __init__(self, config_dir: Path | str = "config") -> None:
        self.config_dir = Path(config_dir)
        self.connectors = ConnectorSettings()
        self.pipeline = PipelineSettings()
        self._yaml_cache: dict[str, Any] = {}

    def _load_yaml(self, filename: str) -> Any:
        if filename not in self._yaml_cache:
            path = self.config_dir / filename
            with open(path) as f:
                self._yaml_cache[filename] = yaml.safe_load(f)
        return self._yaml_cache[filename]

    @property
    def event_types(self) -> dict[str, Any]:
        return self._load_yaml("event_types.yaml")

    @property
    def event_sector_map(self) -> dict[str, Any]:
        return self._load_yaml("event_sector_map.yaml")

    @property
    def regime_rules(self) -> dict[str, Any]:
        return self._load_yaml("regime_rules.yaml")

    @property
    def sector_config(self) -> dict[str, Any]:
        return self._load_yaml("sector_config.yaml")

    @property
    def watchlist(self) -> dict[str, Any]:
        return self._load_yaml("watchlist.yaml")

    @property
    def scenarios(self) -> dict[str, Any]:
        return self._load_yaml("scenarios.yaml")

    def reload(self) -> None:
        """Clear YAML cache to force reload from disk."""
        self._yaml_cache.clear()
