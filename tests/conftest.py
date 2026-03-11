"""Shared test fixtures for InvestorFrame."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pytest

from investorframe.core.config import AppConfig
from investorframe.core.models import (
    AggregateSentiment,
    EconomicDataPoint,
    Event,
    EventContribution,
    MarketRegime,
    MarketSnapshot,
    PipelineResult,
    RawNewsArticle,
    RiskAssessment,
    SectorScore,
    StockScore,
)
from investorframe.core.types import (
    DataSource,
    Direction,
    EventSubtype,
    EventType,
    PipelineStatus,
    RegimeState,
    SentimentLabel,
    Severity,
    SignalLabel,
)


# ── Config ───────────────────────────────────────────────────


@pytest.fixture
def config_dir() -> Path:
    """Return the project config directory."""
    return Path(__file__).parent.parent / "config"


@pytest.fixture
def config(config_dir: Path) -> AppConfig:
    """AppConfig loaded from the real YAML files."""
    return AppConfig(config_dir=config_dir)


# ── Mock Events ──────────────────────────────────────────────


@pytest.fixture
def mock_event_rate_hike() -> Event:
    return Event(
        id="evt_rate_hike",
        event_type=EventType.MONETARY_POLICY,
        subtype=EventSubtype.RATE_DECISION,
        source=DataSource.NEWSAPI,
        timestamp=datetime.now(timezone.utc),
        severity=Severity.HIGH,
        direction=Direction.BEARISH,
        confidence=0.9,
        headline="Fed raises rates by 25 basis points",
        summary="Federal Reserve raises interest rates",
    )


@pytest.fixture
def mock_event_gdp() -> Event:
    return Event(
        id="evt_gdp",
        event_type=EventType.ECONOMIC,
        subtype=EventSubtype.GDP_REPORT,
        source=DataSource.FRED,
        timestamp=datetime.now(timezone.utc),
        severity=Severity.MODERATE,
        direction=Direction.BULLISH,
        confidence=0.85,
        headline="GDP grows 2.5% in Q4",
        summary="US GDP growth exceeded expectations",
    )


@pytest.fixture
def mock_event_oil() -> Event:
    return Event(
        id="evt_oil",
        event_type=EventType.COMMODITY,
        subtype=EventSubtype.OIL_SUPPLY,
        source=DataSource.NEWSAPI,
        timestamp=datetime.now(timezone.utc),
        severity=Severity.HIGH,
        direction=Direction.BULLISH,
        confidence=0.8,
        headline="Oil prices surge on OPEC supply cuts",
    )


@pytest.fixture
def mock_events(
    mock_event_rate_hike: Event,
    mock_event_gdp: Event,
    mock_event_oil: Event,
) -> list[Event]:
    return [mock_event_rate_hike, mock_event_gdp, mock_event_oil]


# ── Mock Market Data ─────────────────────────────────────────


@pytest.fixture
def mock_market_snapshots() -> list[MarketSnapshot]:
    return [
        MarketSnapshot(
            symbol="^GSPC",
            price=5100.0,
            change_pct=0.5,
            volume=3_500_000_000,
            fifty_day_ma=5050.0,
            two_hundred_day_ma=4900.0,
            vix=15.5,
        ),
        MarketSnapshot(
            symbol="^VIX",
            price=15.5,
            change_pct=-2.0,
            volume=0,
        ),
    ]


@pytest.fixture
def mock_economic_data() -> list[EconomicDataPoint]:
    return [
        EconomicDataPoint(
            series_id="T10Y2Y",
            series_name="10Y-2Y Treasury Spread",
            value=0.45,
            date=datetime.now(timezone.utc).date(),
        ),
        EconomicDataPoint(
            series_id="UMCSENT",
            series_name="Consumer Sentiment",
            value=72.0,
            date=datetime.now(timezone.utc).date(),
        ),
    ]


# ── Mock Regime ──────────────────────────────────────────────


@pytest.fixture
def mock_regime_risk_on() -> MarketRegime:
    return MarketRegime(
        state=RegimeState.RISK_ON,
        confidence=0.75,
        contributing_factors=["VIX below 16", "Positive yield curve"],
        indicator_values={"vix": 15.5, "yield_curve": 0.45},
    )


@pytest.fixture
def mock_regime_risk_off() -> MarketRegime:
    return MarketRegime(
        state=RegimeState.RISK_OFF,
        confidence=0.8,
        contributing_factors=["VIX above 28", "Inverted yield curve"],
        indicator_values={"vix": 32.0, "yield_curve": -0.5},
    )


# ── Mock Sector Scores ───────────────────────────────────────


@pytest.fixture
def mock_sector_scores() -> list[SectorScore]:
    return [
        SectorScore(
            symbol="XLK",
            name="Technology",
            score=25.5,
            direction=Direction.BULLISH,
            confidence=0.7,
            rank=1,
            event_count=3,
            driving_events=[
                EventContribution(
                    event_id="e1",
                    headline="AI breakthrough announced",
                    direction=Direction.BULLISH,
                    contribution=2.5,
                    weight=0.8,
                ),
            ],
        ),
        SectorScore(
            symbol="XLF",
            name="Financials",
            score=15.2,
            direction=Direction.BULLISH,
            confidence=0.65,
            rank=2,
            event_count=2,
        ),
        SectorScore(
            symbol="XLE",
            name="Energy",
            score=-10.3,
            direction=Direction.BEARISH,
            confidence=0.6,
            rank=3,
            event_count=2,
        ),
    ]


# ── Mock Stock Scores ────────────────────────────────────────


@pytest.fixture
def mock_stock_scores() -> list[StockScore]:
    return [
        StockScore(
            symbol="AAPL",
            name="Apple Inc.",
            sector="XLK",
            sector_name="Technology",
            tailwind_score=30.0,
            headwind_score=5.0,
            net_signal=25.0,
            label=SignalLabel.TAILWIND,
            confidence=0.7,
            explanation="Tech sector bullish signal",
            rank=1,
        ),
        StockScore(
            symbol="JPM",
            name="JPMorgan Chase",
            sector="XLF",
            sector_name="Financials",
            tailwind_score=15.0,
            headwind_score=3.0,
            net_signal=12.0,
            label=SignalLabel.NEUTRAL,
            confidence=0.65,
            explanation="Financials moderate signal",
            rank=2,
        ),
    ]


# ── Mock Pipeline Result ─────────────────────────────────────


@pytest.fixture
def mock_pipeline_result(
    mock_events: list[Event],
    mock_regime_risk_on: MarketRegime,
    mock_sector_scores: list[SectorScore],
    mock_stock_scores: list[StockScore],
) -> PipelineResult:
    return PipelineResult(
        run_id="test_run_001",
        status=PipelineStatus.COMPLETED,
        started_at=datetime.now(timezone.utc),
        completed_at=datetime.now(timezone.utc),
        duration_seconds=2.5,
        events=mock_events,
        sentiment=AggregateSentiment(
            composite_score=0.25,
            label=SentimentLabel.BULLISH,
            confidence=0.7,
        ),
        regime=mock_regime_risk_on,
        sector_scores=mock_sector_scores,
        stock_scores=mock_stock_scores,
        risk_assessment=RiskAssessment(
            passed=True,
            flags=[],
            disclaimers=["This is for informational purposes only."],
        ),
        connector_status={"fred": "ok", "newsapi": "ok", "yfinance": "ok"},
    )


# ── Mock News Articles ───────────────────────────────────────


@pytest.fixture
def mock_news_articles() -> list[RawNewsArticle]:
    return [
        RawNewsArticle(
            title="Fed raises interest rates by 25 basis points",
            description="The Federal Reserve raised rates as expected",
            source_name="Reuters",
            url="https://example.com/fed-rates",
            published_at=datetime.now(timezone.utc),
        ),
        RawNewsArticle(
            title="Oil prices surge on OPEC cuts",
            description="OPEC announces production cuts",
            source_name="Bloomberg",
            url="https://example.com/oil-prices",
            published_at=datetime.now(timezone.utc),
        ),
    ]
