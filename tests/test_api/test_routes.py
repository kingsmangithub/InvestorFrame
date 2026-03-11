"""Tests for API routes."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from api.dependencies import set_latest_result
from api.main import create_app
from investorframe.core.models import PipelineResult


@pytest.fixture
def client(mock_pipeline_result: PipelineResult) -> TestClient:
    """TestClient with a mock pipeline result loaded."""
    set_latest_result(mock_pipeline_result)
    app = create_app()
    return TestClient(app)


@pytest.fixture
def empty_client() -> TestClient:
    """TestClient with no pipeline result."""
    set_latest_result(None)  # type: ignore[arg-type]
    app = create_app()
    return TestClient(app)


class TestHealthRoute:
    def test_health_returns_ok(self, client: TestClient) -> None:
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "data" in data
        assert data["data"]["version"] == "0.1.0"

    def test_health_without_pipeline(self, empty_client: TestClient) -> None:
        response = empty_client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"


class TestMarketRoute:
    def test_market_returns_data(self, client: TestClient) -> None:
        response = client.get("/api/v1/market")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "data" in data
        assert data["data"]["event_count"] > 0

    def test_market_without_pipeline(self, empty_client: TestClient) -> None:
        response = empty_client.get("/api/v1/market")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "error"


class TestSectorsRoute:
    def test_sectors_returns_data(self, client: TestClient) -> None:
        response = client.get("/api/v1/sectors")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert len(data["data"]["sectors"]) > 0

    def test_sectors_without_pipeline(self, empty_client: TestClient) -> None:
        response = empty_client.get("/api/v1/sectors")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "error"


class TestWatchlistRoute:
    def test_watchlist_returns_data(self, client: TestClient) -> None:
        response = client.get("/api/v1/watchlist")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert data["data"]["total_stocks"] > 0

    def test_watchlist_without_pipeline(self, empty_client: TestClient) -> None:
        response = empty_client.get("/api/v1/watchlist")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "error"


class TestScenariosRoute:
    def test_scenario_with_valid_name(self, client: TestClient) -> None:
        response = client.post(
            "/api/v1/scenarios",
            json={"scenario_name": "fed_rate_hike_50bps"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert data["data"]["scenario_name"] == "fed_rate_hike_50bps"

    def test_scenario_with_invalid_name(self, client: TestClient) -> None:
        response = client.post(
            "/api/v1/scenarios",
            json={"scenario_name": "nonexistent"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "error"

    def test_scenario_without_pipeline(self, empty_client: TestClient) -> None:
        response = empty_client.post(
            "/api/v1/scenarios",
            json={"scenario_name": "fed_rate_hike_50bps"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "error"
