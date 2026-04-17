from investorframe.discipline.behavior import build_behavior_payload
from investorframe.discipline.sell import build_sell_rules_payload
from investorframe.discipline.wisdom import build_wisdom_payload

PRINCIPLES = [
    "Stay inside your circle of competence.",
    "Write the thesis before touching capital.",
    "Always write the anti-thesis.",
    "Price is not the thesis.",
    "No action is a valid action.",
    "Review decisions, not just outcomes.",
    "Protect survival before chasing upside.",
]


def build_rulebook_payload() -> dict:
    behavior = build_behavior_payload()
    sell = build_sell_rules_payload()
    wisdom = build_wisdom_payload()
    return {
        "principles": PRINCIPLES,
        "behavior_gate": behavior["checks"],
        "sell_rules": sell["rules"],
        "wisdom": wisdom,
    }
