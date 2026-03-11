"""FastAPI application factory for InvestorFrame."""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import health, market, scenarios, sectors, watchlist


def create_app() -> FastAPI:
    """Build and configure the FastAPI application."""
    app = FastAPI(
        title="InvestorFrame API",
        version="0.1.0",
        description=(
            "Event-driven market intelligence framework. "
            "Provides regime detection, sector rotation signals, "
            "and watchlist scoring. For informational purposes only."
        ),
    )

    # CORS — permissive for local dev; tighten for production
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register routes
    app.include_router(health.router, tags=["Health"])
    app.include_router(market.router, prefix="/api/v1", tags=["Market"])
    app.include_router(sectors.router, prefix="/api/v1", tags=["Sectors"])
    app.include_router(watchlist.router, prefix="/api/v1", tags=["Watchlist"])
    app.include_router(scenarios.router, prefix="/api/v1", tags=["Scenarios"])

    return app


# uvicorn entrypoint: uvicorn api.main:app
app = create_app()
