from typing import Any, Dict, List, Optional


AI_OUTCOMES = [
    "AI_NOW",
    "AI_LATER",
    "AI_PREPARATION",
    "AI_NOT_JUSTIFIED",
    "AI_INAPPROPRIATE",
]


AI_HUMAN_ROLES = [
    "H0",
    "H1",
    "H2",
    "H3",
]


AI_APPLICATION_TYPES = [
    "AI_ASSISTANCE",
    "AI_AUGMENTATION",
    "AI_AUTOMATION",
    "AI_AGENT",
    "AI_MULTI_AGENT",
]


AI_READINESS_DIMENSIONS = [
    "data",
    "process",
    "documentation",
    "integration",
    "governance",
    "human_role",
    "controls",
    "infrastructure",
]


def evaluate_ai(
    *,
    need: Any,
    task: Any = None,
    alternatives: Any = None,
    solution_evaluation: Any = None,
) -> Dict[str, Any]:
    """
    Evaluate the role of AI after need, capability, reality,
    task and alternative analysis.

    BINAH does not assume that AI is required.

    The evaluation distinguishes between:
    - AI useful now
    - AI useful later
    - AI preparation required
    - AI not justified
    - AI inappropriate

    AI evaluation is a business justification layer, not an
    implementation/runtime layer.
    """

    normalized_need = _normalize_need(need)

    if not normalized_need:
        return {
            "status": "STOP_NEED_NOT_VALIDATED",
            "outcome": "AI_NOT_JUSTIFIED",
            "need": normalized_need,
            "current_opportunities": [],
            "future_opportunities": [],
            "readiness_gaps": [],
            "preparation_plan": [],
            "ai_evolution_path": [],
            "next_action": (
                "Validate the business need before evaluating AI."
            ),
        }

    alternative_data = _extract_alternatives(alternatives)
    solution_data = _extract_solutions(solution_evaluation)

    current_opportunities = _identify_current_ai_opportunities(
        task=task,
        alternatives=alternative_data,
        solutions=solution_data,
    )

    future_opportunities = _identify_future_ai_opportunities(
        task=task,
        alternatives=alternative_data,
        solutions=solution_data,
    )

    readiness_gaps = _identify_readiness_gaps(
        task=task,
        alternatives=alternative_data,
        solutions=solution_data,
    )

    if current_opportunities:
        outcome = "AI_NOW"
    elif future_opportunities:
        outcome = "AI_LATER"
    elif readiness_gaps:
        outcome = "AI_PREPARATION"
    else:
        outcome = "AI_NOT_JUSTIFIED"

    return {
        "status": "AI_EVALUATED",
        "outcome": outcome,
        "need": normalized_need,
        "task": task,
        "current_opportunities": current_opportunities,
        "future_opportunities": future_opportunities,
        "readiness_gaps": readiness_gaps,
        "preparation_plan": [],
        "ai_evolution_path": _default_ai_evolution_path(),
        "human_role": None,
        "recommended_application_type": None,
        "justification": None,
        "risks": [],
        "constraints": [],
        "next_action": (
            "Complete AI opportunity, readiness, human-role and "
            "risk evaluation before implementation."
        ),
    }


def assess_ai_opportunity(
    ai_evaluation: Dict[str, Any],
    *,
    opportunity: str,
    timing: str,
    application_type: str = "AI_ASSISTANCE",
    utility: Any = None,
    value: Any = None,
    evidence: Any = None,
    human_role: str = "H1",
    justification: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Add an explicit AI opportunity to the evaluation.

    timing:
    - NOW
    - LATER
    """

    if timing not in {"NOW", "LATER"}:
        raise ValueError("timing must be NOW or LATER.")

    if application_type not in AI_APPLICATION_TYPES:
        raise ValueError(
            f"Invalid AI application type: {application_type}"
        )

    if human_role not in AI_HUMAN_ROLES:
        raise ValueError(
            f"Invalid human role: {human_role}"
        )

    normalized_opportunity = str(opportunity).strip()

    if not normalized_opportunity:
        raise ValueError("opportunity cannot be empty.")

    opportunity_data = {
        "opportunity": normalized_opportunity,
        "timing": timing,
        "application_type": application_type,
        "utility": utility,
        "value": value,
        "evidence": evidence,
        "human_role": human_role,
        "justification": justification,
    }

    if timing == "NOW":
        ai_evaluation.setdefault(
            "current_opportunities", []
        ).append(opportunity_data)
        ai_evaluation["outcome"] = "AI_NOW"
    else:
        ai_evaluation.setdefault(
            "future_opportunities", []
        ).append(opportunity_data)

        if ai_evaluation.get("outcome") not in {
            "AI_NOW",
        }:
            ai_evaluation["outcome"] = "AI_LATER"

    return ai_evaluation


def assess_readiness_gap(
    ai_evaluation: Dict[str, Any],
    *,
    dimension: str,
    current_state: Any,
    required_state: Any,
    gap: Any,
    priority: str = "MEDIUM",
    preparation_action: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Record a condition that must be addressed before effective
    AI adoption.
    """

    if dimension not in AI_READINESS_DIMENSIONS:
        raise ValueError(
            f"Invalid AI readiness dimension: {dimension}"
        )

    if priority not in {"LOW", "MEDIUM", "HIGH", "CRITICAL"}:
        raise ValueError(
            "priority must be LOW, MEDIUM, HIGH or CRITICAL."
        )

    readiness_gap = {
        "dimension": dimension,
        "current_state": current_state,
        "required_state": required_state,
        "gap": gap,
        "priority": priority,
        "preparation_action": preparation_action,
    }

    ai_evaluation.setdefault(
        "readiness_gaps", []
    ).append(readiness_gap)

    ai_evaluation["outcome"] = (
        "AI_PREPARATION"
        if not ai_evaluation.get("current_opportunities")
        else "AI_NOW"
    )

    return ai_evaluation


def define_preparation_plan(
    ai_evaluation: Dict[str, Any],
    *,
    actions: List[str],
) -> Dict[str, Any]:
    """
    Define the organizational preparation required for future
    or current AI adoption.
    """

    normalized_actions = [
        str(action).strip()
        for action in actions
        if str(action).strip()
    ]

    ai_evaluation["preparation_plan"] = normalized_actions

    if (
        normalized_actions
        and not ai_evaluation.get("current_opportunities")
    ):
        ai_evaluation["outcome"] = "AI_PREPARATION"

    return ai_evaluation


def define_human_role(
    ai_evaluation: Dict[str, Any],
    *,
    human_role: str,
) -> Dict[str, Any]:
    """
    Define the human role in the proposed AI-enabled work.
    """

    if human_role not in AI_HUMAN_ROLES:
        raise ValueError(
            f"Invalid human role: {human_role}"
        )

    ai_evaluation["human_role"] = human_role

    return ai_evaluation


def define_ai_application(
    ai_evaluation: Dict[str, Any],
    *,
    application_type: str,
) -> Dict[str, Any]:
    """
    Define the appropriate AI application level without assuming
    that an autonomous agent is required.
    """

    if application_type not in AI_APPLICATION_TYPES:
        raise ValueError(
            f"Invalid AI application type: {application_type}"
        )

    ai_evaluation["recommended_application_type"] = (
        application_type
    )

    return ai_evaluation


def finalize_ai_evaluation(
    ai_evaluation: Dict[str, Any],
    *,
    outcome: str,
    justification: str,
    risks: Optional[List[str]] = None,
    constraints: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Finalize an AI evaluation using explicit business reasoning.

    This does not implement AI. It records the justified decision
    about the role AI should have in the analyzed situation.
    """

    if outcome not in AI_OUTCOMES:
        raise ValueError(
            f"Invalid AI outcome: {outcome}"
        )

    normalized_justification = str(justification).strip()

    if not normalized_justification:
        raise ValueError(
            "A justification is required to finalize AI evaluation."
        )

    ai_evaluation["outcome"] = outcome
    ai_evaluation["justification"] = normalized_justification
    ai_evaluation["risks"] = list(risks or [])
    ai_evaluation["constraints"] = list(constraints or [])
    ai_evaluation["status"] = "AI_EVALUATION_FINALIZED"

    return ai_evaluation


def validate_ai_evaluation(
    ai_evaluation: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Validate the structure of an AI evaluation.
    """

    errors: List[str] = []

    if not isinstance(ai_evaluation, dict):
        return {
            "valid": False,
            "errors": [
                "ai_evaluation must be a dictionary."
            ],
        }

    if not ai_evaluation.get("need"):
        errors.append("Missing need.")

    outcome = ai_evaluation.get("outcome")

    if outcome is not None and outcome not in AI_OUTCOMES:
        errors.append(
            f"Invalid AI outcome: {outcome}"
        )

    human_role = ai_evaluation.get("human_role")

    if (
        human_role is not None
        and human_role not in AI_HUMAN_ROLES
    ):
        errors.append(
            f"Invalid human role: {human_role}"
        )

    application_type = ai_evaluation.get(
        "recommended_application_type"
    )

    if (
        application_type is not None
        and application_type not in AI_APPLICATION_TYPES
    ):
        errors.append(
            f"Invalid AI application type: {application_type}"
        )

    if not isinstance(
        ai_evaluation.get("current_opportunities", []),
        list,
    ):
        errors.append(
            "current_opportunities must be a list."
        )

    if not isinstance(
        ai_evaluation.get("future_opportunities", []),
        list,
    ):
        errors.append(
            "future_opportunities must be a list."
        )

    if not isinstance(
        ai_evaluation.get("readiness_gaps", []),
        list,
    ):
        errors.append(
            "readiness_gaps must be a list."
        )

    return {
        "valid": len(errors) == 0,
        "errors": errors,
    }


def get_current_ai_opportunities(
    ai_evaluation: Dict[str, Any],
) -> List[Dict[str, Any]]:
    """
    Return AI opportunities that are potentially actionable now.
    """

    return list(
        ai_evaluation.get(
            "current_opportunities",
            [],
        )
    )


def get_future_ai_opportunities(
    ai_evaluation: Dict[str, Any],
) -> List[Dict[str, Any]]:
    """
    Return AI opportunities that should be considered later.
    """

    return list(
        ai_evaluation.get(
            "future_opportunities",
            [],
        )
    )


def get_ai_readiness_gaps(
    ai_evaluation: Dict[str, Any],
) -> List[Dict[str, Any]]:
    """
    Return the organizational gaps that affect AI readiness.
    """

    return list(
        ai_evaluation.get(
            "readiness_gaps",
            [],
        )
    )


def _identify_current_ai_opportunities(
    *,
    task: Any,
    alternatives: List[Any],
    solutions: List[Any],
) -> List[Dict[str, Any]]:
    """
    Identify explicit evidence that AI may be useful now.

    This function does not invent opportunities from absence of data.
    It only uses explicit signals contained in the supplied analysis.
    """

    opportunities: List[Dict[str, Any]] = []

    for item in alternatives + solutions:
        if not isinstance(item, dict):
            continue

        item_type = str(
            item.get("type", "")
        ).upper()

        if item_type != "AI":
            continue

        status = str(
            item.get("status", "")
        ).upper()

        utility = item.get("utility")
        value = item.get("value")
        justification = item.get("justification")

        if (
            status == "EVALUATED"
            and (
                utility
                or value
                or justification
            )
        ):
            opportunities.append(
                {
                    "opportunity": (
                        "AI application identified in the "
                        "evaluated work."
                    ),
                    "timing": "NOW",
                    "application_type": "AI_ASSISTANCE",
                    "utility": utility,
                    "value": value,
                    "evidence": justification,
                    "human_role": item.get(
                        "human_role"
                    ),
                }
            )

    return opportunities


def _identify_future_ai_opportunities(
    *,
    task: Any,
    alternatives: List[Any],
    solutions: List[Any],
) -> List[Dict[str, Any]]:
    """
    Identify AI opportunities that require future conditions.

    The function intentionally does not fabricate a future use case.
    """

    opportunities: List[Dict[str, Any]] = []

    for item in alternatives + solutions:
        if not isinstance(item, dict):
            continue

        item_type = str(
            item.get("type", "")
        ).upper()

        if item_type != "AI":
            continue

        if item.get("status") == "EVALUATED":
            if (
                item.get("utility") is not None
                or item.get("value") is not None
            ):
                opportunities.append(
                    {
                        "opportunity": (
                            "AI may become useful after "
                            "business or operational conditions change."
                        ),
                        "timing": "LATER",
                        "application_type": "AI_AUGMENTATION",
                        "utility": item.get("utility"),
                        "value": item.get("value"),
                        "conditions": [],
                    }
                )

    return opportunities


def _identify_readiness_gaps(
    *,
    task: Any,
    alternatives: List[Any],
    solutions: List[Any],
) -> List[Dict[str, Any]]:
    """
    Identify explicit AI-readiness gaps from available solution data.
    """

    gaps: List[Dict[str, Any]] = []

    for item in alternatives + solutions:
        if not isinstance(item, dict):
            continue

        item_type = str(
            item.get("type", "")
        ).upper()

        if item_type != "AI":
            continue

        if item.get("data_availability") is False:
            gaps.append(
                {
                    "dimension": "data",
                    "current_state": "insufficient",
                    "required_state": "usable AI data",
                    "gap": "Data availability is insufficient.",
                    "priority": "HIGH",
                    "preparation_action": (
                        "Structure and improve the required data."
                    ),
                }
            )

        if item.get("integration") is False:
            gaps.append(
                {
                    "dimension": "integration",
                    "current_state": "not integrated",
                    "required_state": "integrated workflow",
                    "gap": "Required integration is unavailable.",
                    "priority": "MEDIUM",
                    "preparation_action": (
                        "Define the integration requirements."
                    ),
                }
            )

    return gaps


def _extract_alternatives(
    alternatives: Any,
) -> List[Any]:
    if isinstance(alternatives, dict):
        values = alternatives.get(
            "alternatives",
            [],
        )
        return values if isinstance(values, list) else []

    if isinstance(alternatives, list):
        return alternatives

    return []


def _extract_solutions(
    solution_evaluation: Any,
) -> List[Any]:
    if isinstance(solution_evaluation, dict):
        values = solution_evaluation.get(
            "solutions",
            [],
        )
        return values if isinstance(values, list) else []

    if isinstance(solution_evaluation, list):
        return solution_evaluation

    return []


def _normalize_need(need: Any) -> str:
    if isinstance(need, str):
        return need.strip()

    if isinstance(need, dict):
        statement = need.get("statement")

        if statement:
            return str(statement).strip()

        return str(need).strip()

    if need is None:
        return ""

    return str(need).strip()


def _default_ai_evolution_path() -> List[str]:
    return [
        "HUMAN",
        "SOFTWARE",
        "TRADITIONAL_AUTOMATION",
        "AI_ASSISTANCE",
        "AI_AUGMENTATION",
        "AI_AUTOMATION",
        "AI_AGENT",
        "AI_MULTI_AGENT",
        "INTEGRATED_AI",
    ]