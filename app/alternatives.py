from typing import Any, Dict, List


ALTERNATIVE_TYPES = [
    "HUMAN",
    "PROCESS",
    "SOFTWARE",
    "TRADITIONAL_AUTOMATION",
    "AI",
    "HYBRID",
]


ALTERNATIVE_STATUSES = [
    "PENDING_EVALUATION",
    "EVALUATED",
    "RECOMMENDED",
    "NOT_RECOMMENDED",
]


EVALUATION_CRITERIA = [
    "technical_capability",
    "data_availability",
    "reliability",
    "integration",
    "cost",
    "scalability",
    "complexity",
    "technology_dependency",
    "risk",
    "organizational_change",
    "human_role",
    "utility",
    "value",
    "friction",
]


def evaluate_alternatives(
    *,
    need: Any,
    second_decomposition: Any,
) -> Dict[str, Any]:
    """
    Evaluate the available solution alternatives for a validated need.

    BINAH does not assume that AI is the preferred alternative.

    The six alternatives are always considered:

        HUMAN
        PROCESS
        SOFTWARE
        TRADITIONAL_AUTOMATION
        AI
        HYBRID

    This stage prepares the alternatives for comparative evaluation.
    It does not select a solution automatically.
    """

    normalized_need = _normalize_need(need)

    if not normalized_need:
        return {
            "status": "STOP_NEED_NOT_VALIDATED",
            "need": normalized_need,
            "second_decomposition": second_decomposition,
            "alternatives": [],
            "criteria": list(EVALUATION_CRITERIA),
            "evaluated_count": 0,
            "selected_alternative": None,
            "next_action": (
                "Validate the need before evaluating alternatives."
            ),
        }

    alternatives = [
        {
            "type": alternative_type,
            "status": "PENDING_EVALUATION",
            "technical_capability": None,
            "data_availability": None,
            "reliability": None,
            "integration": None,
            "cost": None,
            "scalability": None,
            "complexity": None,
            "technology_dependency": None,
            "risk": None,
            "organizational_change": None,
            "human_role": None,
            "utility": None,
            "value": None,
            "friction": None,
            "justification": None,
        }
        for alternative_type in ALTERNATIVE_TYPES
    ]

    return {
        "status": "READY_FOR_ALTERNATIVE_EVALUATION",
        "need": normalized_need,
        "second_decomposition": second_decomposition,
        "alternatives": alternatives,
        "criteria": list(EVALUATION_CRITERIA),
        "evaluated_count": 0,
        "selected_alternative": None,
        "next_action": (
            "Evaluate human, process, software, traditional automation, "
            "AI, and hybrid alternatives before selecting a solution."
        ),
    }


def evaluate_alternative(
    alternatives_evaluation: Dict[str, Any],
    *,
    alternative_type: str,
    technical_capability: Any = None,
    data_availability: Any = None,
    reliability: Any = None,
    integration: Any = None,
    cost: Any = None,
    scalability: Any = None,
    complexity: Any = None,
    technology_dependency: Any = None,
    risk: Any = None,
    organizational_change: Any = None,
    human_role: Any = None,
    utility: Any = None,
    value: Any = None,
    friction: Any = None,
    justification: Any = None,
) -> Dict[str, Any]:
    """
    Record the evaluation of one alternative.

    Evaluation is evidence-driven. This function records the
    evaluation; it does not automatically recommend AI or any
    other alternative.
    """

    if not isinstance(alternatives_evaluation, dict):
        raise TypeError(
            "alternatives_evaluation must be a dictionary."
        )

    normalized_type = str(alternative_type).strip()

    if normalized_type not in ALTERNATIVE_TYPES:
        raise ValueError(
            f"Invalid alternative type: {normalized_type}"
        )

    alternatives = alternatives_evaluation.setdefault(
        "alternatives",
        [],
    )

    target = None

    for alternative in alternatives:
        if (
            isinstance(alternative, dict)
            and alternative.get("type") == normalized_type
        ):
            target = alternative
            break

    if target is None:
        target = {
            "type": normalized_type,
            "status": "PENDING_EVALUATION",
        }
        alternatives.append(target)

    target.update(
        {
            "status": "EVALUATED",
            "technical_capability": technical_capability,
            "data_availability": data_availability,
            "reliability": reliability,
            "integration": integration,
            "cost": cost,
            "scalability": scalability,
            "complexity": complexity,
            "technology_dependency": technology_dependency,
            "risk": risk,
            "organizational_change": organizational_change,
            "human_role": human_role,
            "utility": utility,
            "value": value,
            "friction": friction,
            "justification": justification,
        }
    )

    alternatives_evaluation["status"] = "EVALUATED"

    alternatives_evaluation["evaluated_count"] = sum(
        1
        for alternative in alternatives
        if isinstance(alternative, dict)
        and alternative.get("status") == "EVALUATED"
    )

    return alternatives_evaluation


def compare_alternatives(
    alternatives_evaluation: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Compare evaluated alternatives.

    No alternative receives preference merely because it uses AI.
    """

    if not isinstance(alternatives_evaluation, dict):
        raise TypeError(
            "alternatives_evaluation must be a dictionary."
        )

    alternatives = alternatives_evaluation.get(
        "alternatives",
        [],
    )

    evaluated = [
        alternative
        for alternative in alternatives
        if isinstance(alternative, dict)
        and alternative.get("status") == "EVALUATED"
    ]

    comparison = []

    for alternative in evaluated:
        comparison.append(
            {
                "type": alternative.get("type"),
                "technical_capability": alternative.get(
                    "technical_capability"
                ),
                "data_availability": alternative.get(
                    "data_availability"
                ),
                "reliability": alternative.get("reliability"),
                "integration": alternative.get("integration"),
                "cost": alternative.get("cost"),
                "scalability": alternative.get("scalability"),
                "complexity": alternative.get("complexity"),
                "technology_dependency": alternative.get(
                    "technology_dependency"
                ),
                "risk": alternative.get("risk"),
                "organizational_change": alternative.get(
                    "organizational_change"
                ),
                "human_role": alternative.get("human_role"),
                "utility": alternative.get("utility"),
                "value": alternative.get("value"),
                "friction": alternative.get("friction"),
                "justification": alternative.get("justification"),
            }
        )

    alternatives_evaluation["comparison"] = comparison

    alternatives_evaluation["status"] = (
        "COMPARISON_READY"
        if evaluated
        else "NO_EVALUATED_ALTERNATIVES"
    )

    alternatives_evaluation["next_action"] = (
        "Select an alternative only when comparative evidence "
        "supports the choice."
    )

    return alternatives_evaluation


def select_alternative(
    alternatives_evaluation: Dict[str, Any],
    *,
    alternative_type: str,
    rationale: str,
) -> Dict[str, Any]:
    """
    Select one evaluated alternative with explicit rationale.

    Selection is permitted only after evaluation.
    """

    if not isinstance(alternatives_evaluation, dict):
        raise TypeError(
            "alternatives_evaluation must be a dictionary."
        )

    normalized_type = str(alternative_type).strip()
    normalized_rationale = str(rationale).strip()

    if normalized_type not in ALTERNATIVE_TYPES:
        raise ValueError(
            f"Invalid alternative type: {normalized_type}"
        )

    if not normalized_rationale:
        raise ValueError(
            "A rationale is required to select an alternative."
        )

    alternatives = alternatives_evaluation.get(
        "alternatives",
        [],
    )

    selected = None

    for alternative in alternatives:
        if (
            isinstance(alternative, dict)
            and alternative.get("type") == normalized_type
            and alternative.get("status") == "EVALUATED"
        ):
            selected = alternative
            break

    if selected is None:
        raise ValueError(
            "Only an evaluated alternative can be selected."
        )

    for alternative in alternatives:
        if (
            isinstance(alternative, dict)
            and alternative.get("status") == "RECOMMENDED"
        ):
            alternative["status"] = "EVALUATED"

    selected["status"] = "RECOMMENDED"
    selected["selection_rationale"] = normalized_rationale

    alternatives_evaluation["selected_alternative"] = selected
    alternatives_evaluation["status"] = "ALTERNATIVE_SELECTED"

    return alternatives_evaluation


def validate_alternatives_evaluation(
    alternatives_evaluation: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Validate the structure of an alternatives evaluation.
    """

    if not isinstance(alternatives_evaluation, dict):
        return {
            "valid": False,
            "errors": [
                "alternatives_evaluation must be a dictionary."
            ],
        }

    errors: List[str] = []

    if "need" not in alternatives_evaluation:
        errors.append("Missing need.")

    if "alternatives" not in alternatives_evaluation:
        errors.append("Missing alternatives.")

    alternatives = alternatives_evaluation.get(
        "alternatives",
        [],
    )

    if not isinstance(alternatives, list):
        errors.append("alternatives must be a list.")
        alternatives = []

    for index, alternative in enumerate(alternatives):
        if not isinstance(alternative, dict):
            errors.append(
                f"Alternative at index {index} must be a dictionary."
            )
            continue

        alternative_type = alternative.get("type")

        if alternative_type not in ALTERNATIVE_TYPES:
            errors.append(
                f"Invalid alternative type at index {index}: "
                f"{alternative_type}"
            )

        status = alternative.get("status")

        if status not in ALTERNATIVE_STATUSES:
            errors.append(
                f"Invalid status at index {index}: {status}"
            )

    return {
        "valid": len(errors) == 0,
        "errors": errors,
    }


def get_selected_alternative(
    alternatives_evaluation: Dict[str, Any],
) -> Any:
    """
    Return the selected alternative, if one exists.
    """

    if not isinstance(alternatives_evaluation, dict):
        return None

    selected = alternatives_evaluation.get(
        "selected_alternative"
    )

    if isinstance(selected, dict):
        return selected

    for alternative in alternatives_evaluation.get(
        "alternatives",
        [],
    ):
        if (
            isinstance(alternative, dict)
            and alternative.get("status") == "RECOMMENDED"
        ):
            return alternative

    return None


def get_evaluated_alternatives(
    alternatives_evaluation: Dict[str, Any],
) -> List[Dict[str, Any]]:
    """
    Return only alternatives that have been evaluated.
    """

    if not isinstance(alternatives_evaluation, dict):
        return []

    return [
        alternative
        for alternative in alternatives_evaluation.get(
            "alternatives",
            [],
        )
        if isinstance(alternative, dict)
        and alternative.get("status") == "EVALUATED"
    ]


def _normalize_need(need: Any) -> str:
    """
    Normalize the need from either a string or BINAH need structure.

    The needs module may return the actual need nested under
    the 'need' property.
    """

    if isinstance(need, str):
        return need.strip()

    if isinstance(need, dict):
        nested_need = need.get("need")

        if isinstance(nested_need, dict):
            statement = nested_need.get("statement")

            if statement:
                return str(statement).strip()

            return str(nested_need).strip()

        statement = need.get("statement")

        if statement:
            return str(statement).strip()

        return str(need).strip()

    if need is None:
        return ""

    return str(need).strip()