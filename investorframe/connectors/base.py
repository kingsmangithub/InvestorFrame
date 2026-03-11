"""Abstract base connector for external data sources."""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import Any, TypeVar

from investorframe.core.config import AppConfig

T = TypeVar("T")
logger = logging.getLogger(__name__)


class ConnectorError(Exception):
    """Raised when a connector fails to fetch data."""


class BaseConnector(ABC):
    """Abstract base for all external data connectors."""

    def __init__(self, config: AppConfig) -> None:
        self.config = config
        self._last_fetch: datetime | None = None
        self._cache: Any = None

    @abstractmethod
    def fetch(self) -> Any:
        """Fetch data from the external source."""
        ...

    @abstractmethod
    def health_check(self) -> bool:
        """Return True if the connector can reach its data source."""
        ...

    @property
    def name(self) -> str:
        return self.__class__.__name__

    def _handle_error(self, error: Exception) -> None:
        logger.error(f"{self.name} failed: {error}")
        raise ConnectorError(f"{self.name}: {error}") from error

    def _update_timestamp(self) -> None:
        self._last_fetch = datetime.now(timezone.utc)
