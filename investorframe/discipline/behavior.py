BEHAVIOR_GATE = [
    "Thesis is written before action.",
    "Anti-thesis is written.",
    "This is not a FOMO-driven action.",
    "I can explain what would prove me wrong.",
    "The position fits my risk budget.",
    "I would still want this after a 48-hour delay.",
]


def build_behavior_payload() -> dict:
    return {"checks": BEHAVIOR_GATE, "default_action": "no_action_if_any_check_fails"}
