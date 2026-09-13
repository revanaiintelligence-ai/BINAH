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
    Evaluate the available solution alternatives after the
    alternatives stage.

    BINAH does not assume that AI is the preferred solution.
    The purpose of this stage is comparative solution evaluation.
    Final AI justification belongs to app.ai.
    """

    normalized_need = _normalize_need(need)
    normalized_alternatives = _extract_alternatives(alternatives)

    if not normalized_need:
        return {
            "status": "STOP_NEED_NOT_VALIDATED",
            "need": normalized_need,
            "solutions": [],
            "result": "AI_NOT_JUSTIFIED",
            "next_action": "Validate the need before evaluating solutions.",
        }

    if not normalized_alternatives:
        return {
            "status": "NO_ALTERNATIVES_AVAILABLE",
            "need": normalized_need,
            "solutions": [],
            "result": "AI_NOT_JUSTIFIED",
            "next_action": (
                "Evaluate the available human, process, software, "
                "traditional automation, AI, and hybrid alternatives."
            ),
        }

    solutions = []

    for alternative in normalized_alternatives:
        if isinstance(alternative, dict):
            alternative_type = alternative.get("type")
            solution = {
                "type": alternative_type,
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
        else:
            solution = {
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

        solutions.append(solution)

    evaluated_count = sum(
        1
        for solution in solutions
        if solution["status"] == "EVALUATED"
    )

    return {
        "status": (
            "EVALUATED"
            if evaluated_count > 0
            else "READY_FOR_SOLUTION_EVALUATION"
        ),
        "need": normalized_need,
        "solutions": solutions,
        "criteria": list(EVALUATION_CRITERIA),
        "evaluated_count": evaluated_count,
        "result": None,
        "selected_solution": None,
        "next_action": (
            "Evaluate each viable alternative and compare "
            "utility, value, risk, friction, and human role."
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

    solutions = solution_evaluation.setdefault("solutions", [])

    normalized_type = str(solution_type).strip()

    target = None

    for solution in solutions:
        if solution.get("type") == normalized_type:
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

    solution_evaluation["status"] = "EVALUATED"

    solution_evaluation["evaluated_count"] = sum(
        1
        for solution in solutions
        if solution.get("status") == "EVALUATED"
    )

    return solution_evaluation


def compare_solutions(
    solution_evaluation: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Compare evaluated solutions without assuming that AI is superior.
    """

    if not isinstance(solution_evaluation, dict):
        raise TypeError("solution_evaluation must be a dictionary.")

    solutions = solution_evaluation.get("solutions", [])

    evaluated = [
        solution
        for solution in solutions
        if solution.get("status") == "EVALUATED"
    ]

    comparison = []

    for solution in evaluated:
        comparison.append(
            {
                "type": solution.get("type"),
                "technical_capability": solution.get(
                    "technical_capability"
                ),
                "reliability": solution.get("reliability"),
                "cost": solution.get("cost"),
                "complexity": solution.get("complexity"),
                "risk": solution.get("risk"),
                "human_role": solution.get("human_role"),
                "utility": solution.get("utility"),
                "value": solution.get("value"),
                "friction": solution.get("friction"),
                "justification": solution.get("justification"),
            }
        )

    solution_evaluation["comparison"] = comparison
    solution_evaluation["status"] = (
        "COMPARISON_READY"
        if evaluated
        else "NO_EVALUATED_SOLUTIONS"
    )

    solution_evaluation["next_action"] = (
        "Select a solution only when the comparative evidence "
        "supports the choice."
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

    This function does not automatically select AI.
    """

    if not isinstance(solution_evaluation, dict):
        raise TypeError("solution_evaluation must be a dictionary.")

    normalized_type = str(solution_type).strip()
    normalized_rationale = str(rationale).strip()

    if not normalized_rationale:
        raise ValueError(
            "A rationale is required to select a solution."
        )

    solutions = solution_evaluation.get("solutions", [])

    selected = None

    for solution in solutions:
        if (
            solution.get("type") == normalized_type
            and solution.get("status") == "EVALUATED"
        ):
            selected = solution
            break

    if selected is None:
        raise ValueError(
            "Only an evaluated solution can be selected."
        )

    for solution in solutions:
        if solution.get("status") == "RECOMMENDED":
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
    Validate the structure of a solution evaluation.
    """

    if not isinstance(solution_evaluation, dict):
        return {
            "valid": False,
            "errors": ["solution_evaluation must be a dictionary."],
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

    return {
        "valid": len(errors) == 0,
        "errors": errors,
    }


def get_recommended_solution(
    solution_evaluation: Dict[str, Any],
) -> Optional[Dict[str, Any]]:
    """
    Return the selected/recommended solution, if one exists.
    """

    selected = solution_evaluation.get("selected_solution")

    if isinstance(selected, dict):
        return selected

    for solution in solution_evaluation.get("solutions", []):
        if solution.get("status") == "RECOMMENDED":
            return solution

    return None


def get_evaluated_solutions(
    solution_evaluation: Dict[str, Any],
) -> List[Dict[str, Any]]:
    """
    Return only evaluated solutions.
    """

    return [
        solution
        for solution in solution_evaluation.get("solutions", [])
        if isinstance(solution, dict)
        and solution.get("status") == "EVALUATED"
    ]


def _extract_alternatives(
    alternatives: Any,
) -> List[Any]:
    """
    Normalize the alternatives stage output.
    """

    if isinstance(alternatives, dict):
        values = alternatives.get("alternatives", [])
        return values if isinstance(values, list) else []

    if isinstance(alternatives, list):
        return alternatives

    return []


def _normalize_need(need: Any) -> str:
    """
    Normalize a need from either a string or BINAH need structure.
    """

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