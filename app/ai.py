from typing import List


def evaluate_ai(
    need: str,
    task: str,
    alternatives: List[str],
) -> dict:
    """Evaluate whether AI is justified after considering alternatives."""

    normalized_alternatives = [
        alternative.strip()
        for alternative in alternatives
        if alternative.strip()
    ]

    return {
        "need": need.strip(),
        "task": task.strip(),
        "alternatives_considered": normalized_alternatives,
        "result": "AI_NOT_JUSTIFIED",
        "reasoning": (
            "AI cannot be justified yet. The need and task must be evaluated "
            "against the available human, process, software, and traditional "
            "automation alternatives before selecting AI."
        ),
        "human_role": "HUMAN_REQUIRED",
        "next_action": (
            "Compare the measurable utility, reliability, cost, risk, "
            "data requirements, and human role of each alternative."
        ),
    }