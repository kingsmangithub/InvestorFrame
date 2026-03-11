"""Watchlist orchestration engine."""

from __future__ import annotations

from investorframe.core.config import AppConfig
from investorframe.core.models import SectorScore, StockScore
from investorframe.watchlist.scorer import StockScorer


class WatchlistEngine:
    """Orchestrates watchlist scoring with optional LLM enrichment."""

    def __init__(self, config: AppConfig, llm: object | None = None) -> None:
        self.config = config
        self.llm = llm
        self.scorer = StockScorer(config)

    def score_watchlist(
        self, sector_scores: list[SectorScore]
    ) -> list[StockScore]:
        """Score all watchlist stocks and optionally enrich with LLM."""
        scores = self.scorer.score_all(sector_scores)

        if self.llm is not None and hasattr(self.llm, "generate_stock_explanation"):
            scores = self._enrich_explanations(scores)

        return scores

    def _enrich_explanations(self, scores: list[StockScore]) -> list[StockScore]:
        """Enhance stock explanations via LLM."""
        enriched = []
        for score in scores:
            try:
                explanation = self.llm.generate_stock_explanation(score, [])  # type: ignore
                if explanation:
                    score = StockScore(
                        symbol=score.symbol,
                        name=score.name,
                        sector=score.sector,
                        sector_name=score.sector_name,
                        tailwind_score=score.tailwind_score,
                        headwind_score=score.headwind_score,
                        net_signal=score.net_signal,
                        label=score.label,
                        confidence=score.confidence,
                        explanation=explanation,
                        driving_events=score.driving_events,
                        sector_score_contribution=score.sector_score_contribution,
                        rank=score.rank,
                    )
            except Exception:
                pass
            enriched.append(score)
        return enriched
