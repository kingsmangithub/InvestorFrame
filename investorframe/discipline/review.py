from investorframe.app.models import ReviewItem

REVIEWS = [
    ReviewItem(
        date="2026-04-10",
        ticker="NVDA",
        result="too_early_exit",
        thesis_quality=7,
        process_quality=5,
        emotional_discipline=3,
        lesson="I sold because the gain felt fragile, not because the thesis deteriorated.",
    ),
    ReviewItem(
        date="2026-04-03",
        ticker="TSLA",
        result="fomo_entry",
        thesis_quality=3,
        process_quality=2,
        emotional_discipline=2,
        lesson="I reacted to price acceleration without a written thesis or exit plan.",
    ),
]


def build_reviews_payload() -> list[dict]:
    return [review.model_dump() for review in REVIEWS]
