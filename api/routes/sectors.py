"""GET /api/v1/sectors — ranked sector scores."""

from __future__ import annotations

from fastapi import APIRouter

from api.dependencies import get_latest_result
from api.schemas import APIMetadata, APIResponse, SectorSummary, SectorsData

router = APIRouter()


@router.get("/sectors", response_model=APIResponse)
async def get_sectors() -> APIResponse:
    """Ranked sector scores with explanations."""
    result = get_latest_result()
    if result is None:
        return APIResponse(
            status="error",
            error="No pipeline results available. Run the pipeline first.",
        )

    sectors = []
    for s in sorted(result.sector_scores, key=lambda x: x.rank):
        sectors.append(
            SectorSummary(
                symbol=s.symbol,
                name=s.name,
                score=s.score,
                direction=s.direction.value,
                confidence=s.confidence,
                rank=s.rank,
                event_count=s.event_count,
                top_drivers=[e.headline for e in s.driving_events[:3]],
            )
        )

    regime_state = "unknown"
    regime_confidence = 0.0
    if result.regime:
        regime_state = result.regime.state.value
        regime_confidence = result.regime.confidence

    return APIResponse(
        status="ok",
        data=SectorsData(
            sectors=sectors,
            regime_state=regime_state,
            regime_confidence=regime_confidence,
            total_sectors=len(sectors),
        ).model_dump(),
        meta=APIMetadata(
            pipeline_run_id=result.run_id,
            data_freshness=result.started_at,
            warnings=result.warnings,
        ),
    )
