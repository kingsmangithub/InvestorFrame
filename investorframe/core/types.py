"""Core type definitions for InvestorFrame."""

from __future__ import annotations

from enum import Enum
try:
    from typing import TypeAlias
except ImportError:
    from typing_extensions import TypeAlias


# ── Enumerations ──────────────────────────────────────────────


class EventType(str, Enum):
    """Top-level event classification."""

    ECONOMIC = "economic"
    GEOPOLITICAL = "geopolitical"
    MONETARY_POLICY = "monetary_policy"
    EARNINGS = "earnings"
    REGULATORY = "regulatory"
    COMMODITY = "commodity"
    LABOR = "labor"
    TRADE = "trade"
    TECHNOLOGY = "technology"
    NATURAL_DISASTER = "natural_disaster"


class EventSubtype(str, Enum):
    """Detailed event sub-classification."""

    # Economic
    GDP_REPORT = "gdp_report"
    INFLATION_DATA = "inflation_data"
    JOBS_REPORT = "jobs_report"
    CONSUMER_CONFIDENCE = "consumer_confidence"
    RETAIL_SALES = "retail_sales"
    HOUSING_DATA = "housing_data"
    PMI = "pmi"
    # Monetary Policy
    RATE_DECISION = "rate_decision"
    FED_SPEECH = "fed_speech"
    QE_QT = "qe_qt"
    # Geopolitical
    CONFLICT = "conflict"
    SANCTIONS = "sanctions"
    ELECTION = "election"
    TRADE_DEAL = "trade_deal"
    # Earnings
    EARNINGS_BEAT = "earnings_beat"
    EARNINGS_MISS = "earnings_miss"
    GUIDANCE_CHANGE = "guidance_change"
    # Regulatory
    NEW_REGULATION = "new_regulation"
    DEREGULATION = "deregulation"
    ANTITRUST = "antitrust"
    # Commodity
    OIL_SUPPLY = "oil_supply"
    METAL_DEMAND = "metal_demand"
    AGRICULTURE = "agriculture"
    # Trade
    TARIFF_CHANGE = "tariff_change"
    TRADE_DEFICIT = "trade_deficit"
    # Technology
    AI_DEVELOPMENT = "ai_development"
    CYBER_INCIDENT = "cyber_incident"
    # Natural Disaster
    WEATHER_EVENT = "weather_event"
    PANDEMIC = "pandemic"


class Direction(str, Enum):
    """Market direction signal."""

    BULLISH = "bullish"
    BEARISH = "bearish"
    NEUTRAL = "neutral"
    MIXED = "mixed"


class RegimeState(str, Enum):
    """Market regime classification."""

    RISK_ON = "risk_on"
    RISK_OFF = "risk_off"
    UNCERTAINTY = "uncertainty"
    TRANSITION = "transition"


class SignalLabel(str, Enum):
    """Watchlist stock signal classification."""

    STRONG_TAILWIND = "strong_tailwind"
    TAILWIND = "tailwind"
    NEUTRAL = "neutral"
    MIXED = "mixed"
    HEADWIND = "headwind"
    STRONG_HEADWIND = "strong_headwind"


class SentimentLabel(str, Enum):
    """Aggregate sentiment classification."""

    VERY_BEARISH = "very_bearish"
    BEARISH = "bearish"
    NEUTRAL = "neutral"
    BULLISH = "bullish"
    VERY_BULLISH = "very_bullish"


class Severity(int, Enum):
    """Event severity level (1-5)."""

    MINIMAL = 1
    LOW = 2
    MODERATE = 3
    HIGH = 4
    CRITICAL = 5


class DataSource(str, Enum):
    """Data source identifier."""

    FRED = "fred"
    NEWSAPI = "newsapi"
    YFINANCE = "yfinance"
    OPENAI = "openai"
    MANUAL = "manual"
    SCENARIO = "scenario"


class PipelineStatus(str, Enum):
    """Pipeline execution status."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    PARTIAL = "partial"
    FAILED = "failed"


# ── Type Aliases ──────────────────────────────────────────────

Confidence: TypeAlias = float  # 0.0 to 1.0
Score: TypeAlias = float  # -100.0 to +100.0
Weight: TypeAlias = float  # 0.0 to 1.0
SectorSymbol: TypeAlias = str  # e.g., "XLK", "XLF"
StockSymbol: TypeAlias = str  # e.g., "AAPL", "JPM"
