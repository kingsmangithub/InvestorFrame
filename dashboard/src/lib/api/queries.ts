import { useQuery, useMutation } from "@tanstack/react-query";
import { fetchMarket, fetchSectors, fetchWatchlist, fetchScenario } from "./client";
import type { ScenarioRequest } from "./types";

export function useMarket() {
  return useQuery({
    queryKey: ["market"],
    queryFn: fetchMarket,
    staleTime: 60_000,
    refetchOnWindowFocus: false,
  });
}

export function useSectors() {
  return useQuery({
    queryKey: ["sectors"],
    queryFn: fetchSectors,
    staleTime: 60_000,
    refetchOnWindowFocus: false,
  });
}

export function useWatchlist() {
  return useQuery({
    queryKey: ["watchlist"],
    queryFn: fetchWatchlist,
    staleTime: 60_000,
    refetchOnWindowFocus: false,
  });
}

export function useScenario() {
  return useMutation({
    mutationFn: (request: ScenarioRequest) => fetchScenario(request),
  });
}
