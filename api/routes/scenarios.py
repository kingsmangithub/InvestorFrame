"""POST /api/v1/scenarios — what-if scenario simulation."""

from __future__ import annotations

from fastapi import APIRouter

from api.dependencies import get_config, get_latest_result
from api.schemas import (
    APIMetadata,
    APIResponse,
    ScenarioData,
    ScenarioRequest,
    ScenarioSectorDelta,
    ScenarioStockDelta,
)
from investorframe.scenarios.simulator import ScenarioSimulator
from investorframe.scenarios.templates import ScenarioTemplateLoader

router = APIRouter()


@router.post("/scenarios", response_model=APIResponse)
async def run_scenario(request: ScenarioRequest) -> APIResponse:
    """Run a what-if scenario simulation against current baseline."""
    result = get_latest_result()
    if result is None:
        return APIResponse(
            status="error",
            error="No pipeline results available. Run the pipeline first.",
        )

    config = get_config()
    loader = ScenarioTemplateLoader(config)

    # Resolve template
    template = None
    if request.scenario_name:
        template = loader.get_template(request.scenario_name)
        if template is None:
            available = loader.list_scenarios()
            return APIResponse(
                status="error",
                error=f"Unknown scenario '{request.scenario_name}'. "
                f"Available: {', '.join(available)}",
            )

    if template is None:
        return APIResponse(
            status="error",
            error="Provide a scenario_name from the predefined templates.",
        )

    # Run simulation
    simulator = ScenarioSimulator(config)
    scenario_result = simulator.simulate(
        template=template,
        baseline_events=result.events,
        baseline_regime=result.regime,
        baseline_sectors=result.sector_scores,
        baseline_stocks=result.stock_scores,
    )

    # Convert to API response
    sector_deltas = [
        ScenarioSectorDelta(
            symbol=si.symbol,
            name=si.name,
            baseline_score=si.baseline_score,
            scenario_score=si.scenario_score,
            delta=si.delta,
            direction_change=si.direction_change,
        )
        for si in scenario_result.sector_impacts
    ]

    stock_deltas = [
        ScenarioStockDelta(
            symbol=wi.symbol,
            name=wi.name,
            baseline_signal=wi.baseline_net_signal,
            scenario_signal=wi.scenario_net_signal,
            delta=wi.delta,
            label_change=wi.label_change,
        )
        for wi in scenario_result.watchlist_impacts
    ]

    return APIResponse(
        status="ok",
        data=ScenarioData(
            scenario_name=scenario_result.scenario_name,
            description=scenario_result.description,
            regime_impact=scenario_result.regime_impact,
            sector_impacts=sector_deltas,
            watchlist_impacts=stock_deltas,
            uncertainty_notes=scenario_result.uncertainty_notes,
        ).model_dump(),
        meta=APIMetadata(
            pipeline_run_id=result.run_id,
            data_freshness=result.started_at,
            warnings=result.warnings,
        ),
    )
