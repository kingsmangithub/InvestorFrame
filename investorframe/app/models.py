from pydantic import BaseModel


class FrameSummary(BaseModel):
    label: str
    confidence: float
    dominant_pressure: str
    caution: str
    action_bias: str


class IdeaCard(BaseModel):
    ticker: str
    company: str
    action: str
    business_summary: str
    bull_case: list[str]
    bear_case: list[str]
    assumptions: list[str]
    invalidation: list[str]
    buy_conditions: list[str]
    sell_conditions: list[str]


class ReviewItem(BaseModel):
    date: str
    ticker: str
    result: str
    thesis_quality: int
    process_quality: int
    emotional_discipline: int
    lesson: str
