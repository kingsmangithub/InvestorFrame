def build_sell_rules_payload() -> dict:
    return {
        "rules": [
            "Sell or trim when the original thesis breaks.",
            "Sell or trim when predefined risk is breached.",
            "Do not average down just to get back to even.",
            "Reallocate only when a materially better idea exists.",
        ]
    }
