import type { BehaviorData, FrameData, IdeaData, ReviewData, RulebookData, WisdomData } from "@/lib/types";

async function fetchJson<T>(path: string): Promise<T> {
  const response = await fetch(path, { headers: { Accept: "application/json" } });
  if (!response.ok) {
    throw new Error(`Failed to load ${path}: ${response.status}`);
  }
  return (await response.json()) as T;
}

export const loadFrame = () => fetchJson<FrameData>("/data/frame.json");
export const loadIdeas = () => fetchJson<IdeaData[]>("/data/ideas.json");
export const loadReviews = () => fetchJson<ReviewData[]>("/data/reviews.json");
export const loadBehavior = () => fetchJson<BehaviorData>("/data/behavior.json");
export const loadRulebook = () => fetchJson<RulebookData>("/data/rulebook.json");
export const loadWisdom = () => fetchJson<WisdomData>("/data/wisdom.json");
