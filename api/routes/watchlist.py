"""GET /api/v1/watchlist — scored watchlist stocks."""

from __future__ import annotations

from fastapi import APIRouter

from api.dependencies import get_latest_result
from api.schemas import APIMetadata, APIResponse, StockSummary, WatchlistData

router = APIRouter()


@router.get("/watchlist", response_model=APIResponse)
async def get_watchlist() -> APIResponse:
    """Scored watchlist with tailwind/headwind labels."""
    result = get_latest_result()
    if result is None:
        return APIResponse(
            status="error",
            error="No pipeline results available. Run the pipeline first.",
        )

    stocks = []
    tailwind_count = 0
    headwind_count = 0
    mixed_count = 0

    for s in sorted(result.stock_scores, key=lambda x: x.rank):
        label_str = s.label.value
        if "tailwind" in label_str:
            tailwind_count += 1
        elif "headwind" in label_str:
            headwind_count += 1
        else:
            mixed_count += 1

        stocks.append(
            StockSummary(
                symbol=s.symbol,
                name=s.name,
                sector=s.sector,
                sector_name=s.sector_name,
                tailwind_score=s.tailwind_score,
                headwind_score=s.headwind_score,
                net_signal=s.net_signal,
                label=label_str,
                confidence=s.confidence,
                explanation=s.explanation,
                rank=s.rank,
                top_drivers=[e.headline for e in s.driving_events[:3]],
            )
        )

    return APIResponse(
        status="ok",
        data=WatchlistData(
            stocks=stocks,
            total_stocks=len(stocks),
            tailwind_count=tailwind_count,
            headwind_count=headwind_count,
            mixed_count=mixed_count,
        ).model_dump(),
        meta=APIMetadata(
            pipeline_run_id=result.run_id,
            data_freshness=result.started_at,
            warnings=result.warnings,
        ),
    )
