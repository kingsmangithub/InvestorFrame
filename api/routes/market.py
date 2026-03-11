"""GET /api/v1/market — regime, sentiment, and active events."""

from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter

from api.dependencies import get_latest_result
from api.schemas import (
    APIMetadata,
    APIResponse,
    MarketData,
    MarketEventSummary,
)

router = APIRouter()


@router.get("/market", response_model=APIResponse)
async def get_market() -> APIResponse:
    """Current market regime, sentiment, and active events."""
    result = get_latest_result()
    if result is None:
        return APIResponse(
            status="error",
            error="No pipeline results available. Run the pipeline first.",
        )

    regime_data = None
    if result.regime:
        regime_data = {
            "state": result.regime.state.value,
            "confidence": result.regime.confidence,
            "contributing_factors": result.regime.contributing_factors,
            "indicator_values": result.regime.indicator_values,
        }

    sentiment_data = None
    if result.sentiment:
        sentiment_data = {
            "composite_score": result.sentiment.composite_score,
            "label": result.sentiment.label.value,
            "confidence": result.sentiment.confidence,
        }

    now = datetime.now(timezone.utc)
    active_events = []
    for e in result.events:
        age_hours = (now - e.timestamp).total_seconds() / 3600
        active_events.append(
            MarketEventSummary(
                id=e.id,
                event_type=e.event_type.value,
                subtype=e.subtype.value,
                severity=e.severity.value,
                direction=e.direction.value,
                headline=e.headline,
                confidence=e.confidence,
                timestamp=e.timestamp,
                age_hours=round(age_hours, 1),
            )
        )

    return APIResponse(
        status="ok",
        data=MarketData(
            regime=regime_data,
            sentiment=sentiment_data,
            active_events=active_events,
            event_count=len(result.events),
        ).model_dump(),
        meta=APIMetadata(
            pipeline_run_id=result.run_id,
            data_freshness=result.started_at,
            warnings=result.warnings,
        ),
    )
