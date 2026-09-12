from typing import List


def evaluate_alternatives(
    need: str,
    alternatives: List[str],
) -> dict:
    return {
        "need": need.strip(),
        "alternatives": [
            {
                "type": alternative.strip(),
                "status": "TO_BE_EVALUATED",
            }
            for alternative in alternatives
        ],
        "next_action": (
            "Evaluate human, process, software, traditional automation, "
            "AI, and hybrid alternatives before selecting a solution."
        ),
    }