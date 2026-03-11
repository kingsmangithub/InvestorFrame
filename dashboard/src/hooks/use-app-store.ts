import { create } from "zustand";

interface AppState {
  market: string;
  horizon: string;
  setMarket: (market: string) => void;
  setHorizon: (horizon: string) => void;
}

export const useAppStore = create<AppState>((set) => ({
  market: "US",
  horizon: "T+3",
  setMarket: (market) => set({ market }),
  setHorizon: (horizon) => set({ horizon }),
}));
