"""NewsAPI connector for news article fetching."""

from __future__ import annotations

import logging
from datetime import datetime, timedelta, timezone

import httpx

from investorframe.connectors.base import BaseConnector
from investorframe.core.config import AppConfig
from investorframe.core.models import RawNewsArticle

logger = logging.getLogger(__name__)

NEWSAPI_BASE_URL = "https://newsapi.org/v2/everything"


class NewsConnector(BaseConnector):
    """Fetches news articles from NewsAPI."""

    DEFAULT_QUERIES: list[str] = [
        "federal reserve",
        "inflation economy",
        "stock market",
        "trade tariff",
        "oil prices",
        "earnings report",
        "geopolitical conflict",
    ]

    def __init__(
        self,
        config: AppConfig,
        queries: list[str] | None = None,
        max_articles_per_query: int = 10,
    ) -> None:
        super().__init__(config)
        self.api_key = config.connectors.newsapi_key
        self.queries = queries or self.DEFAULT_QUERIES
        self.max_articles_per_query = max_articles_per_query
        self.lookback_days = config.pipeline.lookback_days

    def fetch(self) -> list[RawNewsArticle]:
        """Fetch articles for all configured queries."""
        results: list[RawNewsArticle] = []
        seen_urls: set[str] = set()

        for query in self.queries:
            articles = self.fetch_query(query)
            for article in articles:
                if article.url not in seen_urls:
                    seen_urls.add(article.url)
                    results.append(article)

        self._update_timestamp()
        return results

    def fetch_query(self, query: str) -> list[RawNewsArticle]:
        """Fetch articles for a single query."""
        if not self.api_key:
            logger.warning("NewsAPI key not set, skipping query: %s", query)
            return []

        from_date = datetime.now(timezone.utc) - timedelta(days=self.lookback_days)

        params = {
            "q": query,
            "from": from_date.strftime("%Y-%m-%dT%H:%M:%S"),
            "sortBy": "relevancy",
            "pageSize": self.max_articles_per_query,
            "language": "en",
        }
        headers = {"X-Api-Key": self.api_key}

        try:
            resp = httpx.get(
                NEWSAPI_BASE_URL,
                params=params,
                headers=headers,
                timeout=15.0,
            )
            resp.raise_for_status()
            data = resp.json()
        except Exception as exc:
            logger.error("NewsAPI fetch failed for '%s': %s", query, exc)
            return []

        articles: list[RawNewsArticle] = []
        for item in data.get("articles", []):
            try:
                articles.append(
                    RawNewsArticle(
                        title=item.get("title", ""),
                        description=item.get("description"),
                        content=item.get("content"),
                        source_name=item.get("source", {}).get("name", "Unknown"),
                        url=item.get("url", ""),
                        published_at=item.get("publishedAt", datetime.now(timezone.utc).isoformat()),
                        raw_json=item,
                    )
                )
            except Exception as exc:
                logger.debug("Skipping malformed article: %s", exc)

        return articles

    def health_check(self) -> bool:
        """Verify NewsAPI key is valid."""
        if not self.api_key:
            return False
        try:
            headers = {"X-Api-Key": self.api_key}
            params = {"q": "test", "pageSize": 1}
            resp = httpx.get(
                NEWSAPI_BASE_URL,
                params=params,
                headers=headers,
                timeout=10.0,
            )
            return resp.status_code == 200
        except Exception:
            return False
