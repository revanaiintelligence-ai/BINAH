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
    "reliability",
    "complexity",
    "risk",
]


AI_EVALUABLE_SOLUTION_STATUSES = [
    "EVALUATED",
    "RECOMMENDED",
]


def evaluate_ai(
    *,
    need: Any,
    task: Any = None,
    alternatives: Any = None,
    solution_evaluation: Any = None,
) -> Dict[str, Any]:
    """
    Evaluate whether AI is justified for a validated business need.

    BINAH does not assume that AI is the solution.

    The AI decision is based primarily on the comparative
    solution evaluation produced by app.solutions.

    Possible outcomes:
    - AI_NOW
    - AI_LATER
    - AI_PREPARATION
    - AI_NOT_JUSTIFIED
    - AI_INAPPROPRIATE

    If no AI solution has actually been evaluated, the result
    remains pending and outcome is None.
    """

    normalized_need = _normalize_need(need)

    if not normalized_need:
        return _base_result(
            status="STOP_NEED_NOT_VALIDATED",
            outcome="AI_NOT_JUSTIFIED",
            decision_ready=False,
            need="",
            task=task,
            next_action=(
                "Validate the business need before evaluating AI."
            ),
        )

    _ = _extract_alternatives(alternatives)

    solution_data = _extract_solutions(
        solution_evaluation
    )

    evaluated_ai = _get_evaluated_ai_solutions(
        solution_data
    )

    recommended_solution = _get_recommended_solution(
        solution_evaluation
    )

    current_opportunities: List[Dict[str, Any]] = []
    future_opportunities: List[Dict[str, Any]] = []
    readiness_gaps: List[Dict[str, Any]] = []

    # ---------------------------------------------------------
    # 1. Explicitly selected non-AI solution
    # ---------------------------------------------------------

    if recommended_solution:
        selected_type = str(
            recommended_solution.get("type", "")
        ).strip().upper()

        if not _is_ai_solution_type(selected_type):
            return _base_result(
                status="AI_EVALUATED",
                outcome="AI_NOT_JUSTIFIED",
                decision_ready=True,
                need=normalized_need,
                task=task,
                current_opportunities=[],
                future_opportunities=[],
                readiness_gaps=[],
                justification=(
                    "The comparative solution evaluation selected "
                    "a non-AI solution."
                ),
                next_action=(
                    "Proceed with the selected non-AI solution "
                    "and do not introduce AI without a new "
                    "validated need."
                ),
            )

    # ---------------------------------------------------------
    # 2. No evaluated AI solution
    # ---------------------------------------------------------

    if not evaluated_ai:
        return _base_result(
            status="AI_EVALUATION_PENDING",
            outcome=None,
            decision_ready=False,
            need=normalized_need,
            task=task,
            current_opportunities=[],
            future_opportunities=[],
            readiness_gaps=[],
            justification=(
                "No evaluated AI alternative is currently "
                "available in the comparative solution analysis."
            ),
            next_action=(
                "Complete the comparative evaluation of the "
                "AI alternative before making an AI decision."
            ),
        )

    # ---------------------------------------------------------
    # 3. Evaluate explicit AI alternatives
    # ---------------------------------------------------------

    for solution in evaluated_ai:
        current_opportunities.extend(
            _current_opportunities_from_solution(
                solution,
                task=task,
            )
        )

        future_opportunities.extend(
            _future_opportunities_from_solution(
                solution,
                task=task,
            )
        )

        readiness_gaps.extend(
            _readiness_gaps_from_solution(
                solution
            )
        )

    current_opportunities = _unique_dicts(
        current_opportunities
    )

    future_opportunities = _unique_dicts(
        future_opportunities
    )

    readiness_gaps = _unique_dicts(
        readiness_gaps
    )

    # ---------------------------------------------------------
    # 4. Determine outcome
    # ---------------------------------------------------------

    outcome = _determine_outcome(
        evaluated_ai=evaluated_ai,
        current_opportunities=current_opportunities,
        future_opportunities=future_opportunities,
        readiness_gaps=readiness_gaps,
    )

    decision_ready = outcome is not None

    return _base_result(
        status="AI_EVALUATED",
        outcome=outcome,
        decision_ready=decision_ready,
        need=normalized_need,
        task=task,
        current_opportunities=current_opportunities,
        future_opportunities=future_opportunities,
        readiness_gaps=readiness_gaps,
        justification=None,
        next_action=(
            "Complete explicit AI application, human-role, "
            "risk and implementation-condition evaluation "
            "before deployment."
        ),
    )


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
    Add an explicit AI opportunity.

    timing:
    - NOW
    - LATER
    """

    normalized_timing = str(
        timing
    ).strip().upper()

    if normalized_timing not in {"NOW", "LATER"}:
        raise ValueError(
            "timing must be NOW or LATER."
        )

    if application_type not in AI_APPLICATION_TYPES:
        raise ValueError(
            f"Invalid AI application type: {application_type}"
        )

    if human_role not in AI_HUMAN_ROLES:
        raise ValueError(
            f"Invalid human role: {human_role}"
        )

    normalized_opportunity = str(
        opportunity
    ).strip()

    if not normalized_opportunity:
        raise ValueError(
            "opportunity cannot be empty."
        )

    opportunity_data = {
        "opportunity": normalized_opportunity,
        "timing": normalized_timing,
        "application_type": application_type,
        "utility": utility,
        "value": value,
        "evidence": evidence,
        "human_role": human_role,
        "justification": justification,
    }

    if normalized_timing == "NOW":
        ai_evaluation.setdefault(
            "current_opportunities",
            [],
        ).append(opportunity_data)

        ai_evaluation["outcome"] = "AI_NOW"

    else:
        ai_evaluation.setdefault(
            "future_opportunities",
            [],
        ).append(opportunity_data)

        if ai_evaluation.get("outcome") != "AI_NOW":
            ai_evaluation["outcome"] = "AI_LATER"

    ai_evaluation["decision_ready"] = True

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
    Record a condition that must be addressed before
    effective AI adoption.
    """

    if dimension not in AI_READINESS_DIMENSIONS:
        raise ValueError(
            f"Invalid AI readiness dimension: {dimension}"
        )

    normalized_priority = str(
        priority
    ).strip().upper()

    if normalized_priority not in {
        "LOW",
        "MEDIUM",
        "HIGH",
        "CRITICAL",
    }:
        raise ValueError(
            "priority must be LOW, MEDIUM, HIGH or CRITICAL."
        )

    readiness_gap = {
        "dimension": dimension,
        "current_state": current_state,
        "required_state": required_state,
        "gap": gap,
        "priority": normalized_priority,
        "preparation_action": preparation_action,
    }

    ai_evaluation.setdefault(
        "readiness_gaps",
        [],
    ).append(readiness_gap)

    if not ai_evaluation.get(
        "current_opportunities"
    ):
        ai_evaluation["outcome"] = "AI_PREPARATION"

    ai_evaluation["decision_ready"] = True

    return ai_evaluation


def define_preparation_plan(
    ai_evaluation: Dict[str, Any],
    *,
    actions: List[str],
) -> Dict[str, Any]:
    """
    Define preparation actions required for AI adoption.
    """

    normalized_actions = [
        str(action).strip()
        for action in actions
        if str(action).strip()
    ]

    ai_evaluation["preparation_plan"] = (
        normalized_actions
    )

    if (
        normalized_actions
        and not ai_evaluation.get(
            "current_opportunities"
        )
    ):
        ai_evaluation["outcome"] = (
            "AI_PREPARATION"
        )
        ai_evaluation["decision_ready"] = True

    return ai_evaluation


def define_human_role(
    ai_evaluation: Dict[str, Any],
    *,
    human_role: str,
) -> Dict[str, Any]:
    """
    Define the human role in AI-enabled work.
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
    Define the appropriate AI application level.

    A general AI recommendation does not automatically imply
    an autonomous agent.
    """

    if application_type not in AI_APPLICATION_TYPES:
        raise ValueError(
            f"Invalid AI application type: {application_type}"
        )

    ai_evaluation[
        "recommended_application_type"
    ] = application_type

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
    Finalize the AI decision using explicit reasoning.
    """

    if outcome not in AI_OUTCOMES:
        raise ValueError(
            f"Invalid AI outcome: {outcome}"
        )

    normalized_justification = str(
        justification
    ).strip()

    if not normalized_justification:
        raise ValueError(
            "A justification is required to finalize "
            "AI evaluation."
        )

    ai_evaluation["outcome"] = outcome
    ai_evaluation["justification"] = (
        normalized_justification
    )
    ai_evaluation["risks"] = list(
        risks or []
    )
    ai_evaluation["constraints"] = list(
        constraints or []
    )
    ai_evaluation["status"] = (
        "AI_EVALUATION_FINALIZED"
    )
    ai_evaluation["decision_ready"] = True

    return ai_evaluation


def validate_ai_evaluation(
    ai_evaluation: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Validate the structure of an AI evaluation.
    """

    if not isinstance(
        ai_evaluation,
        dict,
    ):
        return {
            "valid": False,
            "errors": [
                "ai_evaluation must be a dictionary."
            ],
        }

    errors: List[str] = []

    if not ai_evaluation.get("need"):
        errors.append("Missing need.")

    outcome = ai_evaluation.get("outcome")

    if (
        outcome is not None
        and outcome not in AI_OUTCOMES
    ):
        errors.append(
            f"Invalid AI outcome: {outcome}"
        )

    decision_ready = ai_evaluation.get(
        "decision_ready"
    )

    if not isinstance(
        decision_ready,
        bool,
    ):
        errors.append(
            "decision_ready must be a boolean."
        )

    human_role = ai_evaluation.get(
        "human_role"
    )

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
            f"Invalid AI application type: "
            f"{application_type}"
        )

    for field in [
        "current_opportunities",
        "future_opportunities",
        "readiness_gaps",
        "preparation_plan",
        "risks",
        "constraints",
    ]:
        if not isinstance(
            ai_evaluation.get(field, []),
            list,
        ):
            errors.append(
                f"{field} must be a list."
            )

    if (
        outcome is None
        and decision_ready is True
    ):
        errors.append(
            "A decision-ready AI evaluation must have "
            "a defined outcome."
        )

    return {
        "valid": len(errors) == 0,
        "errors": errors,
    }


def get_current_ai_opportunities(
    ai_evaluation: Dict[str, Any],
) -> List[Dict[str, Any]]:
    """
    Return AI opportunities potentially actionable now.
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
    Return AI opportunities for later consideration.
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
    Return AI-readiness gaps.
    """

    return list(
        ai_evaluation.get(
            "readiness_gaps",
            [],
        )
    )


def _determine_outcome(
    *,
    evaluated_ai: List[Dict[str, Any]],
    current_opportunities: List[Dict[str, Any]],
    future_opportunities: List[Dict[str, Any]],
    readiness_gaps: List[Dict[str, Any]],
) -> str:
    """
    Determine the AI outcome from explicit comparative evidence.

    Priority:
    1. AI inappropriate
    2. AI now
    3. AI later
    4. AI preparation
    5. AI not justified
    """

    if _ai_is_inappropriate(evaluated_ai):
        return "AI_INAPPROPRIATE"

    if current_opportunities:
        return "AI_NOW"

    if future_opportunities:
        return "AI_LATER"

    if readiness_gaps:
        return "AI_PREPARATION"

    if _ai_was_evaluated_but_not_justified(
        evaluated_ai
    ):
        return "AI_NOT_JUSTIFIED"

    return "AI_NOT_JUSTIFIED"


def _ai_is_inappropriate(
    evaluated_ai: List[Dict[str, Any]],
) -> bool:
    """
    Detect an explicit indication that AI is inappropriate.

    This must be explicit; BINAH must not invent this conclusion.
    """

    for solution in evaluated_ai:
        if solution.get(
            "ai_inappropriate"
        ) is True:
            return True

        for field in [
            "result",
            "result_type",
            "solution_result_type",
        ]:
            result = str(
                solution.get(field, "")
            ).strip().upper()

            if result == "AI_INAPPROPRIATE":
                return True

        justification = str(
            solution.get("justification", "")
        ).strip().upper()

        if justification == "AI_INAPPROPRIATE":
            return True

    return False


def _ai_was_evaluated_but_not_justified(
    evaluated_ai: List[Dict[str, Any]],
) -> bool:
    """
    Confirm that AI was actually evaluated before returning
    AI_NOT_JUSTIFIED.
    """

    return any(
        solution.get("status")
        in AI_EVALUABLE_SOLUTION_STATUSES
        for solution in evaluated_ai
    )


def _current_opportunities_from_solution(
    solution: Dict[str, Any],
    *,
    task: Any = None,
) -> List[Dict[str, Any]]:
    """
    Convert explicit evidence from a solution evaluation
    into current AI opportunities.

    AI_NOW is not inferred from a justification alone.

    A solution can create a current opportunity when:
    - it is explicitly AI_USEFUL or AI_RECOMMENDED, or
    - utility/value contains an explicit positive signal,
    - and timing is not explicitly LATER,
    - and there is no explicit blocking condition.
    """

    if solution.get("timing") == "LATER":
        return []

    if not _solution_is_currently_ready(solution):
        return []

    result_types = {
        str(
            solution.get(field, "")
        ).strip().upper()
        for field in [
            "result",
            "result_type",
            "solution_result_type",
        ]
    }

    explicit_ai_result = bool(
        result_types
        & {
            "AI_USEFUL",
            "AI_RECOMMENDED",
        }
    )

    utility = solution.get("utility")
    value = solution.get("value")

    explicit_positive_signal = (
        _has_positive_signal(utility)
        or _has_positive_signal(value)
    )

    if not (
        explicit_ai_result
        or explicit_positive_signal
    ):
        return []

    return [
        {
            "opportunity": (
                "AI application identified in the "
                "evaluated solution."
            ),
            "timing": "NOW",
            "application_type": (
                solution.get(
                    "application_type"
                )
                or "AI_ASSISTANCE"
            ),
            "utility": utility,
            "value": value,
            "evidence": solution.get(
                "justification"
            ),
            "human_role": solution.get(
                "human_role"
            ),
            "task": task,
        }
    ]


def _future_opportunities_from_solution(
    solution: Dict[str, Any],
    *,
    task: Any = None,
) -> List[Dict[str, Any]]:
    """
    Convert an explicitly later AI opportunity into a
    future AI opportunity.

    AI_LATER is never invented merely because readiness is
    incomplete.
    """

    if solution.get("timing") != "LATER":
        return []

    utility = solution.get("utility")
    value = solution.get("value")

    result_types = {
        str(
            solution.get(field, "")
        ).strip().upper()
        for field in [
            "result",
            "result_type",
            "solution_result_type",
        ]
    }

    explicit_ai_result = bool(
        result_types
        & {
            "AI_OPTIONAL",
            "AI_USEFUL",
            "AI_RECOMMENDED",
        }
    )

    if not (
        explicit_ai_result
        or _has_positive_signal(utility)
        or _has_positive_signal(value)
    ):
        return []

    return [
        {
            "opportunity": (
                "AI opportunity explicitly identified "
                "for later consideration."
            ),
            "timing": "LATER",
            "application_type": (
                solution.get(
                    "application_type"
                )
                or "AI_AUGMENTATION"
            ),
            "utility": utility,
            "value": value,
            "conditions": [],
            "human_role": solution.get(
                "human_role"
            ),
            "task": task,
        }
    ]


def _readiness_gaps_from_solution(
    solution: Dict[str, Any],
) -> List[Dict[str, Any]]:
    """
    Convert explicit solution constraints into AI-readiness gaps.

    Only explicit False values are treated as insufficient.
    """

    gaps: List[Dict[str, Any]] = []

    dimension_values = {
        "data": solution.get(
            "data_availability"
        ),
        "integration": solution.get(
            "integration"
        ),
        "reliability": solution.get(
            "reliability"
        ),
        "complexity": solution.get(
            "complexity"
        ),
        "risk": solution.get(
            "risk"
        ),
        "human_role": solution.get(
            "human_role"
        ),
    }

    for dimension, value in dimension_values.items():
        if value is False:
            gaps.append(
                {
                    "dimension": dimension,
                    "current_state": "insufficient",
                    "required_state": (
                        "sufficient for effective "
                        "AI use"
                    ),
                    "gap": (
                        f"{dimension} is insufficient "
                        "for effective AI use."
                    ),
                    "priority": "HIGH",
                    "preparation_action": (
                        f"Improve {dimension} before "
                        "AI adoption."
                    ),
                }
            )

    return gaps


def _solution_is_currently_ready(
    solution: Dict[str, Any],
) -> bool:
    """
    Determine whether an evaluated AI solution has explicit
    blockers preventing a current AI opportunity.

    Only explicit False values block current consideration.
    """

    blocking_dimensions = [
        "data_availability",
        "integration",
        "reliability",
        "risk",
    ]

    for dimension in blocking_dimensions:
        if solution.get(dimension) is False:
            return False

    return True


def _get_evaluated_ai_solutions(
    solutions: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """
    Return explicitly evaluable AI solutions.

    Both EVALUATED and RECOMMENDED are valid here.

    RECOMMENDED is included because app.solutions.select_solution()
    changes the selected solution status from EVALUATED to
    RECOMMENDED.
    """

    evaluated: List[Dict[str, Any]] = []

    for solution in solutions:
        if not isinstance(
            solution,
            dict,
        ):
            continue

        status = str(
            solution.get("status", "")
        ).strip().upper()

        if status not in AI_EVALUABLE_SOLUTION_STATUSES:
            continue

        solution_type = str(
            solution.get("type", "")
        ).strip().upper()

        if _is_ai_solution_type(
            solution_type
        ):
            evaluated.append(solution)
            continue

        if solution.get("is_ai") is True:
            evaluated.append(solution)
            continue

        application_type = str(
            solution.get(
                "application_type",
                ""
            )
        ).strip().upper()

        if application_type in AI_APPLICATION_TYPES:
            evaluated.append(solution)

    return evaluated


def _is_ai_solution_type(
    solution_type: str,
) -> bool:
    """
    Detect the canonical AI solution type used by app.solutions.
    """

    normalized = str(
        solution_type
    ).strip().upper()

    return (
        normalized == "AI"
        or normalized.startswith("AI_")
    )


def _get_recommended_solution(
    solution_evaluation: Any,
) -> Optional[Dict[str, Any]]:
    """
    Return an explicitly selected solution.
    """

    if not isinstance(
        solution_evaluation,
        dict,
    ):
        return None

    for field in [
        "selected_solution",
        "recommended_solution",
        "recommendation",
    ]:
        selected = solution_evaluation.get(
            field
        )

        if isinstance(
            selected,
            dict,
        ):
            return selected

    for solution in solution_evaluation.get(
        "solutions",
        [],
    ):
        if (
            isinstance(
                solution,
                dict,
            )
            and str(
                solution.get("status", "")
            ).strip().upper()
            == "RECOMMENDED"
        ):
            return solution

    return None


def _extract_solutions(
    solution_evaluation: Any,
) -> List[Any]:
    """
    Normalize the output from app.solutions.
    """

    if isinstance(
        solution_evaluation,
        dict,
    ):
        solutions = solution_evaluation.get(
            "solutions",
            []
        )

        if isinstance(
            solutions,
            list,
        ):
            return solutions

    if isinstance(
        solution_evaluation,
        list,
    ):
        return solution_evaluation

    return []


def _extract_alternatives(
    alternatives: Any,
) -> List[Any]:
    """
    Normalize the alternatives-stage output.
    """

    if isinstance(
        alternatives,
        dict,
    ):
        values = alternatives.get(
            "alternatives",
            []
        )

        if isinstance(
            values,
            list,
        ):
            return values

    if isinstance(
        alternatives,
        list,
    ):
        return alternatives

    return []


def _normalize_need(
    need: Any,
) -> str:
    """
    Normalize a need from either a string or BINAH need structure.

    Supports the nested structure returned by app.needs.
    """

    if isinstance(
        need,
        str,
    ):
        return need.strip()

    if isinstance(
        need,
        dict,
    ):
        nested_need = need.get("need")

        if isinstance(
            nested_need,
            dict,
        ):
            statement = nested_need.get(
                "statement"
            )

            if statement:
                return str(
                    statement
                ).strip()

        if isinstance(
            nested_need,
            str,
        ):
            return nested_need.strip()

        statement = need.get(
            "statement"
        )

        if statement:
            return str(
                statement
            ).strip()

        return str(need).strip()

    if need is None:
        return ""

    return str(need).strip()


def _has_positive_signal(
    value: Any,
) -> bool:
    """
    Determine whether an evaluation field contains
    an explicit positive signal.

    False and None are not positive signals.
    """

    if value is None:
        return False

    if value is False:
        return False

    if isinstance(
        value,
        (int, float),
    ):
        return value > 0

    if isinstance(
        value,
        str,
    ):
        normalized = value.strip().lower()

        return normalized in {
            "true",
            "yes",
            "si",
            "sí",
            "positive",
            "positive_signal",
            "useful",
            "high",
            "medium",
            "recommended",
            "valuable",
            "high_value",
        }

    return bool(value)


def _base_result(
    *,
    status: str,
    outcome: Optional[str],
    decision_ready: bool,
    need: str,
    task: Any = None,
    current_opportunities: Optional[
        List[Dict[str, Any]]
    ] = None,
    future_opportunities: Optional[
        List[Dict[str, Any]]
    ] = None,
    readiness_gaps: Optional[
        List[Dict[str, Any]]
    ] = None,
    preparation_plan: Optional[
        List[str]
    ] = None,
    justification: Optional[str] = None,
    risks: Optional[
        List[str]
    ] = None,
    constraints: Optional[
        List[str]
    ] = None,
    next_action: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Build the common AI evaluation structure.
    """

    return {
        "status": status,
        "outcome": outcome,
        "decision_ready": decision_ready,
        "need": need,
        "task": task,
        "current_opportunities": (
            current_opportunities or []
        ),
        "future_opportunities": (
            future_opportunities or []
        ),
        "readiness_gaps": (
            readiness_gaps or []
        ),
        "preparation_plan": (
            preparation_plan or []
        ),
        "ai_evolution_path": (
            _default_ai_evolution_path()
        ),
        "human_role": None,
        "recommended_application_type": None,
        "justification": justification,
        "risks": risks or [],
        "constraints": constraints or [],
        "next_action": next_action,
    }


def _default_ai_evolution_path() -> List[str]:
    """
    Default evolution path for AI adoption.

    The path is conditional, not a prediction.
    """

    return [
        "Need validation",
        "Comparative solution evaluation",
        "AI suitability evaluation",
        "AI readiness",
        "Human role definition",
        "Application level definition",
        "Controlled implementation",
        "Monitoring and reassessment",
    ]


def _unique_dicts(
    values: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """
    Remove duplicate dictionaries while preserving order.
    """

    unique: List[Dict[str, Any]] = []
    seen = set()

    for value in values:
        key = repr(
            sorted(
                value.items(),
                key=lambda item: str(item[0]),
            )
        )

        if key in seen:
            continue

        seen.add(key)
        unique.append(value)

    return unique