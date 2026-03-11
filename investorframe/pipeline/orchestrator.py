"""Full daily pipeline orchestrator."""

from __future__ import annotations

import logging
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed

from investorframe.connectors.fred import FredConnector
from investorframe.connectors.llm import LLMConnector
from investorframe.connectors.market import MarketConnector
from investorframe.connectors.news import NewsConnector
from investorframe.core.config import AppConfig
from investorframe.core.db import Database
from investorframe.core.models import MarketRegime, PipelineResult
from investorframe.core.types import PipelineStatus, RegimeState
from investorframe.events.classifier import EventClassifier
from investorframe.events.parser import EventParser
from investorframe.pipeline.context import PipelineContext
from investorframe.regime.detector import RegimeDetector
from investorframe.risk.gates import RiskGateRunner
from investorframe.sectors.engine import SectorScoringEngine
from investorframe.sentiment.aggregator import SentimentAggregator
from investorframe.sentiment.analyzer import SentimentAnalyzer
from investorframe.watchlist.scorer import StockScorer

logger = logging.getLogger(__name__)


class PipelineOrchestrator:
    """Runs the full analysis pipeline in phased sequence.

    Phase 1: Data collection (parallel — FRED, NewsAPI, yfinance)
    Phase 2: Event processing (parse + classify)
    Phase 3: Market state   (sentiment + regime in parallel)
    Phase 4: Scoring        (sectors then watchlist, sequential)
    Phase 5: Risk & output  (risk gates, optional persistence)
    """

    def __init__(
        self,
        config: AppConfig,
        db: Database | None = None,
    ) -> None:
        self.config = config
        self.db = db

        # Connectors
        self.fred = FredConnector(config)
        self.news = NewsConnector(config)
        self.market = MarketConnector(config)
        self.llm: LLMConnector | None = (
            LLMConnector(config) if config.pipeline.enable_llm else None
        )

        # Processors
        self.parser = EventParser(config)
        self.classifier = EventClassifier(config, llm=self.llm)
        self.sentiment_analyzer = SentimentAnalyzer(config, llm=self.llm)
        self.sentiment_aggregator = SentimentAggregator()
        self.regime_detector = RegimeDetector(config)
        self.sector_engine = SectorScoringEngine(config)
        self.stock_scorer = StockScorer(config)
        self.risk_gates = RiskGateRunner(config)

    def run(self) -> PipelineResult:
        """Execute the full pipeline and return a PipelineResult."""
        ctx = PipelineContext(run_id=uuid.uuid4().hex[:16])
        logger.info("Pipeline run %s started", ctx.run_id)

        try:
            self._phase_1_collect(ctx)
            self._phase_2_events(ctx)
            self._phase_3_market_state(ctx)
            self._phase_4_scoring(ctx)
            self._phase_5_risk(ctx)

            ctx.status = (
                PipelineStatus.COMPLETED
                if not ctx.errors
                else PipelineStatus.PARTIAL
            )
        except Exception as exc:
            logger.exception("Pipeline failed: %s", exc)
            ctx.add_error(str(exc))
            ctx.status = PipelineStatus.FAILED

        result = ctx.to_result()
        self._persist(result)

        logger.info(
            "Pipeline run %s finished — status=%s, events=%d, sectors=%d, stocks=%d",
            result.run_id,
            result.status.value,
            len(result.events),
            len(result.sector_scores),
            len(result.stock_scores),
        )
        return result

    # ── Phase 1: Data Collection ─────────────────────────────────

    def _phase_1_collect(self, ctx: PipelineContext) -> None:
        """Fetch data from all connectors in parallel."""
        logger.info("Phase 1: Collecting data from connectors")

        def fetch_fred() -> None:
            data = self.fred.fetch()
            if data is not None:
                ctx.economic_data = data
                ctx.connector_status["fred"] = "ok"
            else:
                ctx.connector_status["fred"] = "no_data"
                ctx.add_warning("FRED connector returned no data")

        def fetch_news() -> None:
            articles = self.news.fetch()
            if articles is not None:
                ctx.raw_articles = articles
                ctx.connector_status["newsapi"] = "ok"
            else:
                ctx.connector_status["newsapi"] = "no_data"
                ctx.add_warning("News connector returned no data")

        def fetch_market() -> None:
            snapshots = self.market.fetch()
            if snapshots is not None:
                ctx.market_data = snapshots
                ctx.connector_status["yfinance"] = "ok"
            else:
                ctx.connector_status["yfinance"] = "no_data"
                ctx.add_warning("Market connector returned no data")

        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = {
                executor.submit(fetch_fred): "fred",
                executor.submit(fetch_news): "newsapi",
                executor.submit(fetch_market): "yfinance",
            }
            for future in as_completed(futures):
                source = futures[future]
                try:
                    future.result()
                except Exception as exc:
                    ctx.connector_status[source] = f"failed: {exc}"
                    ctx.add_warning(f"{source} connector failed: {exc}")
                    logger.warning("%s connector failed: %s", source, exc)

    # ── Phase 2: Event Processing ────────────────────────────────

    def _phase_2_events(self, ctx: PipelineContext) -> None:
        """Parse raw data into events, then classify."""
        logger.info("Phase 2: Processing events")
        news_events = self.parser.parse_news_articles(ctx.raw_articles)
        econ_events = self.parser.parse_economic_data(ctx.economic_data)
        all_events = news_events + econ_events

        classified = self.classifier.classify_batch(all_events)

        # Enforce max_events limit
        max_events = self.config.pipeline.max_events
        if len(classified) > max_events:
            classified.sort(key=lambda e: e.effective_severity, reverse=True)
            classified = classified[:max_events]
            ctx.add_warning(
                f"Truncated events from {len(all_events)} to {max_events}"
            )

        ctx.events = classified
        logger.info("Phase 2 complete: %d events classified", len(ctx.events))

    # ── Phase 3: Market State ────────────────────────────────────

    def _phase_3_market_state(self, ctx: PipelineContext) -> None:
        """Sentiment analysis and regime detection in parallel."""
        logger.info("Phase 3: Analyzing market state")

        def analyze_sentiment() -> None:
            event_signal = self.sentiment_analyzer.analyze_events(ctx.events)
            news_signal = self.sentiment_analyzer.analyze_news(ctx.raw_articles)
            market_signal = self.sentiment_analyzer.analyze_market_data(
                ctx.market_data
            )
            ctx.sentiment = self.sentiment_aggregator.aggregate(
                [event_signal, news_signal, market_signal]
            )

        def detect_regime() -> None:
            ctx.regime = self.regime_detector.detect(
                ctx.market_data, ctx.economic_data
            )

        with ThreadPoolExecutor(max_workers=2) as executor:
            sent_future = executor.submit(analyze_sentiment)
            regime_future = executor.submit(detect_regime)
            for f in as_completed([sent_future, regime_future]):
                try:
                    f.result()
                except Exception as exc:
                    ctx.add_warning(f"Market state analysis error: {exc}")
                    logger.warning("Phase 3 error: %s", exc)

    # ── Phase 4: Scoring ─────────────────────────────────────────

    def _phase_4_scoring(self, ctx: PipelineContext) -> None:
        """Score sectors then watchlist stocks (sequential)."""
        logger.info("Phase 4: Scoring")

        # Ensure regime exists
        if ctx.regime is None:
            ctx.add_warning("No regime detected; defaulting to UNCERTAINTY")
            ctx.regime = MarketRegime(
                state=RegimeState.UNCERTAINTY,
                confidence=0.3,
                contributing_factors=["Default: no indicator data available"],
            )

        ctx.sector_scores = self.sector_engine.score_all(
            ctx.events, ctx.regime
        )
        ctx.stock_scores = self.stock_scorer.score_all(ctx.sector_scores)

        logger.info(
            "Phase 4 complete: %d sectors, %d stocks scored",
            len(ctx.sector_scores),
            len(ctx.stock_scores),
        )

    # ── Phase 5: Risk & Output ───────────────────────────────────

    def _phase_5_risk(self, ctx: PipelineContext) -> None:
        """Run risk gates against accumulated results."""
        logger.info("Phase 5: Risk evaluation")
        result = ctx.to_result()
        ctx.risk_assessment = self.risk_gates.assess(result)

        if not ctx.risk_assessment.passed:
            ctx.add_warning("Risk assessment did not pass all gates")

    # ── Persistence ──────────────────────────────────────────────

    def _persist(self, result: PipelineResult) -> None:
        """Store results to database if available."""
        if self.db is None:
            return
        try:
            from investorframe.core.db import (
                EventRecord,
                PipelineRunRecord,
                RegimeRecord,
                SectorScoreRecord,
                StockScoreRecord,
            )

            with self.db.get_session() as session:
                run_record = PipelineRunRecord(
                    run_id=result.run_id,
                    status=result.status.value,
                    started_at=result.started_at,
                    completed_at=result.completed_at,
                    duration_seconds=result.duration_seconds,
                    event_count=len(result.events),
                    sector_count=len(result.sector_scores),
                    stock_count=len(result.stock_scores),
                    warnings="; ".join(result.warnings),
                    errors="; ".join(result.errors),
                )
                session.add(run_record)

                if result.regime:
                    regime_rec = RegimeRecord(
                        run_id=result.run_id,
                        state=result.regime.state.value,
                        confidence=result.regime.confidence,
                    )
                    session.add(regime_rec)

                for sector in result.sector_scores:
                    session.add(
                        SectorScoreRecord(
                            run_id=result.run_id,
                            symbol=sector.symbol,
                            name=sector.name,
                            score=sector.score,
                            direction=sector.direction.value,
                            confidence=sector.confidence,
                            rank=sector.rank,
                        )
                    )

                for stock in result.stock_scores:
                    session.add(
                        StockScoreRecord(
                            run_id=result.run_id,
                            symbol=stock.symbol,
                            name=stock.name,
                            sector=stock.sector,
                            net_signal=stock.net_signal,
                            label=stock.label.value,
                            confidence=stock.confidence,
                            rank=stock.rank,
                        )
                    )

                session.commit()
                logger.info("Persisted run %s to database", result.run_id)
        except Exception as exc:
            logger.warning("Database persistence failed: %s", exc)
