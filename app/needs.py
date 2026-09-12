from typing import Any, Dict, List


NEED_TYPES = [
    "problem",
    "missing_capability",
    "opportunity",
    "speed",
    "precision",
    "information",
    "coordination",
    "scale",
    "operational_capacity",
    "required_condition",
]


def identify_need(
    *,
    business: str,
    context: str,
    objective: str,
    business_map: Dict[str, Any],
    evidence: Any = None,
) -> Dict[str, Any]:
    """
    Identify and structure a real business need.

    BINAH principle:
    Need before AI.

    A need is not automatically equivalent to a problem.
    The purpose of this module is to structure the need so that
    capability, gap, reality, and solution analysis can follow.
    """

    business_name = business.strip()
    business_context = context.strip()
    business_objective = objective.strip()

    if not business_name:
        raise ValueError("Business is required.")

    if not business_objective:
        raise ValueError("Objective is required.")

    return {
        "status": "NEED_IDENTIFIED",
        "business": business_name,
        "context": business_context,
        "objective": business_objective,
        "need": {
            "statement": None,
            "type": None,
            "area": None,
            "function": None,
            "process": None,
            "activity": None,
            "task": None,
            "actor": None,
        },
        "evidence": _normalize_evidence(evidence),
        "need_types": NEED_TYPES,
        "business_map_available": bool(business_map),
        "validation": {
            "identified": False,
            "validated": False,
            "reason": "Need requires explicit identification and evidence.",
        },
    }


def define_need(
    analysis: Dict[str, Any],
    *,
    statement: str,
    need_type: str,
    area: str = "",
    function: str = "",
    process: str = "",
    activity: str = "",
    task: str = "",
    actor: str = "",
) -> Dict[str, Any]:
    """
    Define a specific need inside the preliminary analysis.
    """

    need_statement = statement.strip()
    normalized_type = need_type.strip().lower()

    if not need_statement:
        raise ValueError("Need statement is required.")

    if normalized_type not in NEED_TYPES:
        raise ValueError(
            f"Invalid need type: {need_type}"
        )

    updated = dict(analysis)

    updated["need"] = {
        "statement": need_statement,
        "type": normalized_type,
        "area": area.strip(),
        "function": function.strip(),
        "process": process.strip(),
        "activity": activity.strip(),
        "task": task.strip(),
        "actor": actor.strip(),
    }

    updated["validation"] = {
        "identified": True,
        "validated": False,
        "reason": (
            "Need identified. Reality Gate must determine "
            "whether the need is sufficiently validated."
        ),
    }

    updated["status"] = "READY_FOR_CAPABILITY_DIAGNOSIS"

    return updated


def validate_need_definition(
    analysis: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Validate that a need has been explicitly defined.
    """

    errors: List[str] = []

    need = analysis.get("need", {})

    if not need.get("statement"):
        errors.append("Need statement is missing.")

    if not need.get("type"):
        errors.append("Need type is missing.")

    return {
        "valid": not errors,
        "errors": errors,
        "status": "VALID" if not errors else "INVALID",
    }


def get_need_statement(
    analysis: Dict[str, Any],
) -> str:
    """
    Return the normalized need statement.
    """

    need = analysis.get("need", {})
    return str(need.get("statement") or "").strip()


def _normalize_evidence(
    evidence: Any,
) -> List[Any]:
    """
    Normalize evidence into a list without assigning evidentiary
    validity. Evidence quality is evaluated later by the Reality Gate.
    """

    if evidence is None:
        return []

    if isinstance(evidence, list):
        return evidence

    return [evidence]