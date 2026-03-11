import type {
  APIResponse,
  MarketData,
  SectorsData,
  WatchlistData,
  ScenarioData,
  ScenarioRequest,
  HealthData,
} from "./types";
import {
  mockMarketData,
  mockSectorsData,
  mockWatchlistData,
  getMockScenarioResult,
} from "@/mocks";

const API_BASE = "/api/v1";

// Set to true to use mock data (Phase 1)
const USE_MOCK = true;

async function fetchAPI<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });

  if (!response.ok) {
    throw new Error(`API error: ${response.status} ${response.statusText}`);
  }

  const envelope: APIResponse<T> = await response.json();

  if (envelope.status === "error") {
    throw new Error(envelope.error ?? "Unknown API error");
  }

  return envelope.data;
}

export async function fetchMarket(): Promise<MarketData> {
  if (USE_MOCK) {
    await delay(600);
    return mockMarketData;
  }
  return fetchAPI<MarketData>("/market");
}

export async function fetchSectors(): Promise<SectorsData> {
  if (USE_MOCK) {
    await delay(800);
    return mockSectorsData;
  }
  return fetchAPI<SectorsData>("/sectors");
}

export async function fetchWatchlist(): Promise<WatchlistData> {
  if (USE_MOCK) {
    await delay(700);
    return mockWatchlistData;
  }
  return fetchAPI<WatchlistData>("/watchlist");
}

export async function fetchScenario(request: ScenarioRequest): Promise<ScenarioData> {
  if (USE_MOCK) {
    await delay(1200);
    const result = getMockScenarioResult(request.scenario_name);
    if (!result) throw new Error(`Unknown scenario: ${request.scenario_name}`);
    return result;
  }
  return fetchAPI<ScenarioData>("/scenarios", {
    method: "POST",
    body: JSON.stringify(request),
  });
}

export async function fetchHealth(): Promise<HealthData> {
  if (USE_MOCK) {
    return {
      version: "0.1.0",
      uptime_seconds: 3600,
      last_pipeline_run: new Date().toISOString(),
      last_pipeline_status: "completed",
      database_status: "ok",
    };
  }
  return fetchAPI<HealthData>("/health");
}

function delay(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}
