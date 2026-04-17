from investorframe.frame.regime import build_default_frame


def build_frame_payload() -> dict:
    frame = build_default_frame()
    return {
        "date": "2026-04-17",
        "frame": frame.model_dump(),
        "questions": [
            "What changed?",
            "What is still unclear?",
            "What deserves patience today?",
        ],
    }
