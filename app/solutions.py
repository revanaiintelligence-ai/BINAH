from typing import Any, Dict, List, Optional


SOLUTION_STATUSES = [
    "PENDING_EVALUATION",
    "EVALUATED",
    "RECOMMENDED",
    "NOT_RECOMMENDED",
]


SOLUTION_RESULT_TYPES = [
    "NON_AI_SOLUTION_RECOMMENDED",
    "PROCESS_IMPROVEMENT_RECOMMENDED",
    "SOFTWARE_RECOMMENDED",
    "TRADITIONAL_AUTOMATION_RECOMMENDED",
    "AI_OPTIONAL",
    "AI_USEFUL",
    "AI_RECOMMENDED",
    "AI_NOT_JUSTIFIED",
    "AI_INAPPROPRIATE",
    "HYBRID_SOLUTION_RECOMMENDED",
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


def evaluate_solutions(
    *,
    need: Any,
    alternatives: Any,
) -> Dict[str, Any]:
    """
    Prepare the available alternatives for comparative solution evaluation.

    BINAH does not assume that AI is the preferred solution.

    This stage:
    1. validates that a need exists,
    2. normalizes the alternatives,
    3. exposes the evaluation criteria,
    4. preserves supplied evaluations,
    5. does not invent a recommendation.

    Final AI justification belongs to app.ai.
    Final diagnostic consolidation belongs to app.diagnostic.
    """

    normalized_need = _normalize_need(need)
    normalized_alternatives = _extract_alternatives(alternatives)

    if not normalized_need:
        return {
            "status": "STOP_NEED_NOT_VALIDATED",
            "need": "",
            "solutions": [],
            "criteria": list(EVALUATION_CRITERIA),
            "evaluated_count": 0,
            "comparison": [],
            "result": None,
            "selected_solution": None,
            "next_action": (
                "Validate the need before evaluating solution alternatives."
            ),
        }

    if not normalized_alternatives:
        return {
            "status": "NO_ALTERNATIVES_AVAILABLE",
            "need": normalized_need,
            "solutions": [],
            "criteria": list(EVALUATION_CRITERIA),
            "evaluated_count": 0,
            "comparison": [],
            "result": None,
            "selected_solution": None,
            "next_action": (
                "Evaluate the available human, process, software, "
                "traditional automation, AI, and hybrid alternatives."
            ),
        }

    solutions = []

    for alternative in normalized_alternatives:
        solution = _normalize_solution(alternative)

        if solution.get("type"):
            solutions.append(solution)

    evaluated_count = sum(
        1
        for solution in solutions
        if solution.get("status") == "EVALUATED"
    )

    status = (
        "EVALUATED"
        if evaluated_count > 0
        else "READY_FOR_SOLUTION_EVALUATION"
    )

    result = None

    if evaluated_count == len(solutions) and evaluated_count > 0:
        status = "COMPARISON_READY"

    return {
        "status": status,
        "need": normalized_need,
        "solutions": solutions,
        "criteria": list(EVALUATION_CRITERIA),
        "evaluated_count": evaluated_count,
        "comparison": [],
        "result": result,
        "selected_solution": None,
        "next_action": (
            "Evaluate and compare viable alternatives before selecting "
            "a solution."
        ),
    }


def evaluate_solution(
    solution_evaluation: Dict[str, Any],
    *,
    solution_type: str,
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
    Record the evaluation of one solution alternative.
    """

    if not isinstance(solution_evaluation, dict):
        raise TypeError("solution_evaluation must be a dictionary.")

    normalized_type = str(solution_type).strip()

    if not normalized_type:
        raise ValueError("solution_type cannot be empty.")

    solutions = solution_evaluation.setdefault("solutions", [])

    target = None

    for solution in solutions:
        if (
            isinstance(solution, dict)
            and solution.get("type") == normalized_type
        ):
            target = solution
            break

    if target is None:
        target = {
            "type": normalized_type,
            "status": "PENDING_EVALUATION",
        }
        solutions.append(target)

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

    solution_evaluation["evaluated_count"] = sum(
        1
        for solution in solutions
        if isinstance(solution, dict)
        and solution.get("status") == "EVALUATED"
    )

    if solution_evaluation["evaluated_count"] > 0:
        solution_evaluation["status"] = "EVALUATED"

    return solution_evaluation


def compare_solutions(
    solution_evaluation: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Build a comparison of evaluated solutions.

    This function does not select a winner and does not infer
    that AI is preferable.
    """

    if not isinstance(solution_evaluation, dict):
        raise TypeError("solution_evaluation must be a dictionary.")

    solutions = solution_evaluation.get("solutions", [])

    if not isinstance(solutions, list):
        raise TypeError("solution_evaluation['solutions'] must be a list.")

    evaluated = [
        solution
        for solution in solutions
        if isinstance(solution, dict)
        and solution.get("status") == "EVALUATED"
    ]

    comparison = []

    for solution in evaluated:
        comparison.append(
            {
                "type": solution.get("type"),
                "technical_capability": solution.get(
                    "technical_capability"
                ),
                "data_availability": solution.get(
                    "data_availability"
                ),
                "reliability": solution.get("reliability"),
                "integration": solution.get("integration"),
                "cost": solution.get("cost"),
                "scalability": solution.get("scalability"),
                "complexity": solution.get("complexity"),
                "technology_dependency": solution.get(
                    "technology_dependency"
                ),
                "risk": solution.get("risk"),
                "organizational_change": solution.get(
                    "organizational_change"
                ),
                "human_role": solution.get("human_role"),
                "utility": solution.get("utility"),
                "value": solution.get("value"),
                "friction": solution.get("friction"),
                "justification": solution.get("justification"),
            }
        )

    solution_evaluation["comparison"] = comparison

    if evaluated:
        solution_evaluation["status"] = "COMPARISON_READY"
        solution_evaluation["next_action"] = (
            "Select a solution only when comparative evidence "
            "supports the choice."
        )
    else:
        solution_evaluation["status"] = "NO_EVALUATED_SOLUTIONS"
        solution_evaluation["next_action"] = (
            "Evaluate viable alternatives before comparing or "
            "selecting a solution."
        )

    return solution_evaluation


def select_solution(
    solution_evaluation: Dict[str, Any],
    *,
    solution_type: str,
    rationale: str,
    result: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Select one evaluated solution with an explicit rationale.

    Selection is explicit. BINAH does not automatically select AI.
    """

    if not isinstance(solution_evaluation, dict):
        raise TypeError("solution_evaluation must be a dictionary.")

    normalized_type = str(solution_type).strip()
    normalized_rationale = str(rationale).strip()

    if not normalized_type:
        raise ValueError("solution_type cannot be empty.")

    if not normalized_rationale:
        raise ValueError(
            "A rationale is required to select a solution."
        )

    solutions = solution_evaluation.get("solutions", [])

    if not isinstance(solutions, list):
        raise TypeError("solution_evaluation['solutions'] must be a list.")

    selected = None

    for solution in solutions:
        if (
            isinstance(solution, dict)
            and solution.get("type") == normalized_type
            and solution.get("status") == "EVALUATED"
        ):
            selected = solution
            break

    if selected is None:
        raise ValueError(
            "Only an evaluated solution can be selected."
        )

    for solution in solutions:
        if (
            isinstance(solution, dict)
            and solution.get("status") == "RECOMMENDED"
        ):
            solution["status"] = "EVALUATED"

    selected["status"] = "RECOMMENDED"
    selected["selection_rationale"] = normalized_rationale

    solution_evaluation["selected_solution"] = selected

    if result is not None:
        normalized_result = str(result).strip()

        if normalized_result not in SOLUTION_RESULT_TYPES:
            raise ValueError(
                f"Invalid solution result type: {normalized_result}"
            )

        solution_evaluation["result"] = normalized_result

    solution_evaluation["status"] = "SOLUTION_SELECTED"

    return solution_evaluation


def validate_solution_evaluation(
    solution_evaluation: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Validate the structural integrity of a solution evaluation.
    """

    if not isinstance(solution_evaluation, dict):
        return {
            "valid": False,
            "errors": [
                "solution_evaluation must be a dictionary."
            ],
        }

    errors: List[str] = []

    if "need" not in solution_evaluation:
        errors.append("Missing need.")

    if "solutions" not in solution_evaluation:
        errors.append("Missing solutions.")

    solutions = solution_evaluation.get("solutions", [])

    if not isinstance(solutions, list):
        errors.append("solutions must be a list.")
        solutions = []

    for index, solution in enumerate(solutions):
        if not isinstance(solution, dict):
            errors.append(
                f"Solution at index {index} must be a dictionary."
            )
            continue

        if not solution.get("type"):
            errors.append(
                f"Solution at index {index} is missing type."
            )

        status = solution.get("status")

        if status not in SOLUTION_STATUSES:
            errors.append(
                f"Invalid status for solution at index {index}: "
                f"{status}"
            )

    result = solution_evaluation.get("result")

    if result is not None and result not in SOLUTION_RESULT_TYPES:
        errors.append(
            f"Invalid solution result type: {result}"
        )

    return {
        "valid": len(errors) == 0,
        "errors": errors,
    }


def get_recommended_solution(
    solution_evaluation: Dict[str, Any],
) -> Optional[Dict[str, Any]]:
    """
    Return the explicitly selected/recommended solution, if one exists.
    """

    if not isinstance(solution_evaluation, dict):
        return None

    selected = solution_evaluation.get("selected_solution")

    if isinstance(selected, dict):
        return selected

    for solution in solution_evaluation.get("solutions", []):
        if (
            isinstance(solution, dict)
            and solution.get("status") == "RECOMMENDED"
        ):
            return solution

    return None


def get_evaluated_solutions(
    solution_evaluation: Dict[str, Any],
) -> List[Dict[str, Any]]:
    """
    Return only evaluated solutions.
    """

    if not isinstance(solution_evaluation, dict):
        return []

    solutions = solution_evaluation.get("solutions", [])

    if not isinstance(solutions, list):
        return []

    return [
        solution
        for solution in solutions
        if isinstance(solution, dict)
        and solution.get("status") == "EVALUATED"
    ]


def _normalize_solution(
    alternative: Any,
) -> Dict[str, Any]:
    """
    Normalize one alternative into the solution-evaluation structure.
    """

    if isinstance(alternative, dict):
        alternative_type = alternative.get("type")

        if alternative_type is None:
            alternative_type = alternative.get("name")

        solution = {
            "type": (
                str(alternative_type).strip()
                if alternative_type is not None
                else ""
            ),
            "status": alternative.get(
                "status",
                "PENDING_EVALUATION",
            ),
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

        return solution

    return {
        "type": str(alternative).strip(),
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


def _extract_alternatives(
    alternatives: Any,
) -> List[Any]:
    """
    Normalize the alternatives-stage output.
    """

    if isinstance(alternatives, dict):
        values = alternatives.get("alternatives", [])

        if isinstance(values, list):
            return values

        return []

    if isinstance(alternatives, list):
        return alternatives

    return []


def _normalize_need(
    need: Any,
) -> str:
    """
    Normalize a need from either a string or BINAH need structure.

    BINAH needs may arrive directly or nested under the 'need' key.
    """

    if isinstance(need, str):
        return need.strip()

    if isinstance(need, dict):
        nested_need = need.get("need")

        if isinstance(nested_need, dict):
            statement = nested_need.get("statement")

            if statement:
                return str(statement).strip()

        if isinstance(nested_need, str):
            return nested_need.strip()

        statement = need.get("statement")

        if statement:
            return str(statement).strip()

        return str(need).strip()

    if need is None:
        return ""

    return str(need).strip()