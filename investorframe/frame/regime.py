from investorframe.app.models import FrameSummary


def build_default_frame() -> FrameSummary:
    return FrameSummary(
        label="mixed",
        confidence=0.62,
        dominant_pressure="Rates have eased, but crowding in AI leaders keeps risk asymmetric.",
        caution="Do not confuse narrative strength with guaranteed future returns.",
        action_bias="Selective. Prefer waiting over forcing action.",
    )
