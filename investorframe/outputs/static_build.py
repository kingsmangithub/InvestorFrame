from investorframe.app.config import DATA_DIR
from investorframe.app.storage import write_json
from investorframe.discipline.behavior import build_behavior_payload
from investorframe.discipline.review import build_reviews_payload
from investorframe.discipline.rulebook import build_rulebook_payload
from investorframe.discipline.sell import build_sell_rules_payload
from investorframe.discipline.thesis import build_ideas_payload
from investorframe.discipline.wisdom import build_wisdom_payload
from investorframe.frame.summary import build_frame_payload


def main() -> None:
    write_json(DATA_DIR / "frame.json", build_frame_payload())
    write_json(DATA_DIR / "ideas.json", build_ideas_payload())
    write_json(DATA_DIR / "behavior.json", build_behavior_payload())
    write_json(DATA_DIR / "sell_rules.json", build_sell_rules_payload())
    write_json(DATA_DIR / "reviews.json", build_reviews_payload())
    write_json(DATA_DIR / "rulebook.json", build_rulebook_payload())
    write_json(DATA_DIR / "wisdom.json", build_wisdom_payload())
    print(f"Wrote static payloads to {DATA_DIR}")


if __name__ == "__main__":
    main()
