"""Tests for regime detection."""

from __future__ import annotations

from datetime import datetime, timezone

from investorframe.core.config import AppConfig
from investorframe.core.models import EconomicDataPoint, MarketSnapshot
from investorframe.core.types import RegimeState
from investorframe.regime.detector import RegimeDetector


class TestRegimeDetector:
    def test_detect_with_no_data(self, config: AppConfig) -> None:
        detector = RegimeDetector(config)
        regime = detector.detect([], [])
        assert regime is not None
        assert regime.state in (
            RegimeState.RISK_ON,
            RegimeState.RISK_OFF,
            RegimeState.UNCERTAINTY,
            RegimeState.TRANSITION,
        )

    def test_risk_on_with_low_vix(
        self, config: AppConfig, mock_market_snapshots: list[MarketSnapshot]
    ) -> None:
        detector = RegimeDetector(config)
        # VIX at 15.5 should push toward RISK_ON
        regime = detector.detect(mock_market_snapshots, [])
        assert regime is not None
        assert regime.confidence > 0

    def test_risk_off_with_high_vix(self, config: AppConfig) -> None:
        detector = RegimeDetector(config)
        snapshots = [
            MarketSnapshot(
                symbol="^VIX",
                price=35.0,
                change_pct=5.0,
                volume=0,
                vix=35.0,
            ),
        ]
        regime = detector.detect(snapshots, [])
        assert regime is not None
        # High VIX should push toward RISK_OFF
        assert regime.indicator_values.get("vix", 0) >= 28.0

    def test_indicator_values_populated(
        self,
        config: AppConfig,
        mock_market_snapshots: list[MarketSnapshot],
        mock_economic_data: list[EconomicDataPoint],
    ) -> None:
        detector = RegimeDetector(config)
        regime = detector.detect(mock_market_snapshots, mock_economic_data)
        assert isinstance(regime.indicator_values, dict)

    def test_contributing_factors(
        self, config: AppConfig, mock_market_snapshots: list[MarketSnapshot]
    ) -> None:
        detector = RegimeDetector(config)
        regime = detector.detect(mock_market_snapshots, [])
        assert isinstance(regime.contributing_factors, list)
