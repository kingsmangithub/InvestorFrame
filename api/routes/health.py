"""GET /health — system health and connector status."""

from __future__ import annotations

from fastapi import APIRouter

import investorframe
from api.dependencies import get_latest_result, get_uptime
from api.schemas import APIResponse, ConnectorHealth, HealthData

router = APIRouter()


@router.get("/health", response_model=APIResponse)
async def health_check() -> APIResponse:
    """System health with connector status and last pipeline info."""
    result = get_latest_result()

    connectors: list[ConnectorHealth] = []
    last_run = None
    last_status = None

    if result is not None:
        last_run = result.started_at
        last_status = result.status.value
        for name, status in result.connector_status.items():
            connectors.append(
                ConnectorHealth(
                    name=name,
                    status="ok" if status == "ok" else "degraded",
                    last_success=result.started_at if status == "ok" else None,
                )
            )

    return APIResponse(
        status="ok",
        data=HealthData(
            version=investorframe.__version__,
            uptime_seconds=round(get_uptime(), 1),
            last_pipeline_run=last_run,
            last_pipeline_status=last_status,
            connectors=connectors,
        ).model_dump(),
    )
