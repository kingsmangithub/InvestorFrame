"""Tests for scenario simulation."""

from __future__ import annotations

from investorframe.core.config import AppConfig
from investorframe.core.models import Event, MarketRegime, SectorScore, StockScore
from investorframe.scenarios.simulator import ScenarioSimulator
from investorframe.scenarios.templates import ScenarioTemplateLoader


class TestScenarioSimulator:
    def test_simulate_predefined_scenario(
        self,
        config: AppConfig,
        mock_events: list[Event],
        mock_regime_risk_on: MarketRegime,
        mock_sector_scores: list[SectorScore],
        mock_stock_scores: list[StockScore],
    ) -> None:
        loader = ScenarioTemplateLoader(config)
        template = loader.get_template("fed_rate_hike_50bps")
        assert template is not None

        simulator = ScenarioSimulator(config)
        result = simulator.simulate(
            template=template,
            baseline_events=mock_events,
            baseline_regime=mock_regime_risk_on,
            baseline_sectors=mock_sector_scores,
            baseline_stocks=mock_stock_scores,
        )
        assert result.scenario_name == "fed_rate_hike_50bps"
        assert len(result.sector_impacts) > 0
        assert len(result.uncertainty_notes) > 0

    def test_scenario_computes_deltas(
        self,
        config: AppConfig,
        mock_events: list[Event],
        mock_regime_risk_on: MarketRegime,
        mock_sector_scores: list[SectorScore],
        mock_stock_scores: list[StockScore],
    ) -> None:
        loader = ScenarioTemplateLoader(config)
        template = loader.get_template("oil_price_shock")
        assert template is not None

        simulator = ScenarioSimulator(config)
        result = simulator.simulate(
            template=template,
            baseline_events=mock_events,
            baseline_regime=mock_regime_risk_on,
            baseline_sectors=mock_sector_scores,
            baseline_stocks=mock_stock_scores,
        )
        # Sector impacts should have delta values
        for si in result.sector_impacts:
            assert hasattr(si, "delta")
            assert isinstance(si.delta, float)


class TestScenarioTemplateLoader:
    def test_list_scenarios(self, config: AppConfig) -> None:
        loader = ScenarioTemplateLoader(config)
        scenarios = loader.list_scenarios()
        assert len(scenarios) >= 8
        assert "fed_rate_hike_50bps" in scenarios
        assert "oil_price_shock" in scenarios

    def test_get_template(self, config: AppConfig) -> None:
        loader = ScenarioTemplateLoader(config)
        template = loader.get_template("fed_rate_hike_50bps")
        assert template is not None
        assert template.name == "fed_rate_hike_50bps"
        assert len(template.events) > 0

    def test_get_unknown_template(self, config: AppConfig) -> None:
        loader = ScenarioTemplateLoader(config)
        template = loader.get_template("nonexistent_scenario")
        assert template is None

    def test_get_all_templates(self, config: AppConfig) -> None:
        loader = ScenarioTemplateLoader(config)
        all_templates = loader.get_all_templates()
        assert len(all_templates) >= 8
