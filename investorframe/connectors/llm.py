"""OpenAI LLM connector for optional enrichment tasks."""

from __future__ import annotations

import json
import logging
from typing import Any

from investorframe.connectors.base import BaseConnector
from investorframe.core.config import AppConfig
from investorframe.core.models import Event, StockScore

logger = logging.getLogger(__name__)


class LLMConnector(BaseConnector):
    """Optional OpenAI integration for classification and explanation."""

    def __init__(self, config: AppConfig) -> None:
        super().__init__(config)
        self.api_key = config.connectors.openai_api_key
        self.model = config.connectors.openai_model
        self.enabled = config.pipeline.enable_llm and bool(self.api_key)

    def fetch(self) -> None:
        """Not used directly -- LLM connector is called on-demand."""
        return None

    def classify_headline(
        self, headline: str, description: str = ""
    ) -> dict[str, Any]:
        """Classify a news headline into event type, direction, severity.

        Returns dict with keys: event_type, subtype, direction, severity, confidence.
        """
        if not self.enabled:
            return {}

        prompt = (
            "Classify this market news headline. Return JSON with keys: "
            "event_type, subtype, direction (bullish/bearish/neutral), "
            "severity (1-5), confidence (0.0-1.0).\n\n"
            f"Headline: {headline}\n"
        )
        if description:
            prompt += f"Description: {description}\n"

        result = self._call_openai(prompt)
        try:
            return json.loads(result)
        except (json.JSONDecodeError, TypeError):
            logger.warning("LLM classification parse failed for: %s", headline)
            return {}

    def generate_stock_explanation(
        self,
        stock: StockScore,
        driving_events: list[Event],
    ) -> str:
        """Generate a natural language explanation for a stock's score."""
        if not self.enabled:
            return ""

        events_text = "\n".join(
            f"- {e.headline} (severity={e.severity.value}, direction={e.direction.value})"
            for e in driving_events[:5]
        )

        prompt = (
            f"Explain in 2-3 sentences why {stock.symbol} ({stock.name}) "
            f"has a {stock.label.value} signal (net score: {stock.net_signal:.1f}).\n"
            f"Driving events:\n{events_text}\n"
            "Be concise, factual, and avoid investment advice."
        )

        return self._call_openai(prompt)

    def enrich_event_summary(self, event: Event) -> str:
        """Generate a concise summary of an event's market implications."""
        if not self.enabled:
            return ""

        prompt = (
            f"Summarize the market implications of this event in 1-2 sentences:\n"
            f"Type: {event.event_type.value}/{event.subtype.value}\n"
            f"Headline: {event.headline}\n"
            f"Direction: {event.direction.value}\n"
            "Be factual and concise."
        )

        return self._call_openai(prompt)

    def _call_openai(self, prompt: str) -> str:
        """Make a single OpenAI API call."""
        try:
            from openai import OpenAI

            client = OpenAI(api_key=self.api_key)
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a financial market analyst. Be concise and factual."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.3,
                max_tokens=300,
            )
            return response.choices[0].message.content or ""
        except Exception as exc:
            logger.error("OpenAI call failed: %s", exc)
            return ""

    def health_check(self) -> bool:
        """Verify OpenAI API key is valid."""
        if not self.api_key:
            return False
        try:
            from openai import OpenAI

            client = OpenAI(api_key=self.api_key)
            client.models.list()
            return True
        except Exception:
            return False
