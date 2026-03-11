"""FastAPI dependency injection for InvestorFrame."""

from __future__ import annotations

import time
from functools import lru_cache

from investorframe.core.config import AppConfig
from investorframe.core.db import Database
from investorframe.core.models import PipelineResult

# Module-level state
_app_start_time: float = time.time()
_latest_result: PipelineResult | None = None


@lru_cache(maxsize=1)
def get_config() -> AppConfig:
    """Singleton AppConfig."""
    return AppConfig()


@lru_cache(maxsize=1)
def get_db() -> Database:
    """Singleton Database."""
    config = get_config()
    db = Database(url=config.pipeline.db_url)
    db.create_tables()
    return db


def get_latest_result() -> PipelineResult | None:
    """Return the most recent pipeline result (in-memory cache)."""
    return _latest_result


def set_latest_result(result: PipelineResult) -> None:
    """Store a pipeline result for API consumption."""
    global _latest_result
    _latest_result = result


def get_uptime() -> float:
    """Return seconds since the API started."""
    return time.time() - _app_start_time
