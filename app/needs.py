"""
BINAH — Need Analysis

Need identification and structuring layer for BINAH v0.2.

Core principle:
    Need before AI.

This module does not validate the business need.
It identifies a preliminary need candidate from the available
business information and evidence.

Reality validation remains the responsibility of reality.py.
"""

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
    Identify a preliminary business-need candidate.

    This function does not claim that the need has been validated.

    Sources used:
    - business
    - context
    - objective
    - business map
    - explicitly structured evidence

    If evidence contains an explicit need statement, that statement
    is used as the primary candidate.

    Otherwise, the objective is used only to construct a provisional
    need hypothesis. The hypothesis must still pass the Reality Gate.
    """

    business_name = _normalize_text(business)
    business_context = _normalize_text(context)
    business_objective = _normalize_text(objective)

    if not business_name:
        raise ValueError("Business is required.")

    if not business_objective:
        raise ValueError("Objective is required.")

    normalized_evidence = _normalize_evidence(evidence)

    explicit_need = _extract_explicit_need(normalized_evidence)

    if explicit_need:
        need = _build_need_from_evidence(explicit_need)
        status = "NEED_CANDIDATE_IDENTIFIED"
        reason = (
            "A need statement was found in the supplied evidence. "
            "Reality Gate must determine whether it is sufficiently "
            "validated."
        )
    else:
        need = {
            "statement": _build_need_hypothesis(
                objective=business_objective
            ),
            "type": None,
            "area": "",
            "function": "",
            "process": "",
            "activity": "",
            "task": "",
            "actor": "",
        }

        status = "NEED_HYPOTHESIS"
        reason = (
            "No explicit need statement was supplied. "
            "A provisional hypothesis was derived from the objective. "
            "Additional evidence or clarification is required before "
            "the need can be considered validated."
        )

    return {
        "status": status,
        "business": business_name,
        "context": business_context,
        "objective": business_objective,
        "need": need,
        "evidence": normalized_evidence,
        "need_types": NEED_TYPES,
        "business_map_available": bool(business_map),
        "validation": {
            "identified": bool(need.get("statement")),
            "validated": False,
            "reason": reason,
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
    Explicitly define a specific business need.

    This function converts a preliminary candidate into a structured
    need definition. It still does not validate the need.
    """

    need_statement = _normalize_text(statement)
    normalized_type = _normalize_text(need_type).lower()

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
        "area": _normalize_text(area),
        "function": _normalize_text(function),
        "process": _normalize_text(process),
        "activity": _normalize_text(activity),
        "task": _normalize_text(task),
        "actor": _normalize_text(actor),
    }

    updated["validation"] = {
        "identified": True,
        "validated": False,
        "reason": (
            "Need explicitly defined. Reality Gate must determine "
            "whether the need is sufficiently validated."
        ),
    }

    updated["status"] = "READY_FOR_CAPABILITY_DIAGNOSIS"

    return updated


def validate_need_definition(
    analysis: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Validate whether a structured need definition is present.

    This is structural validation only.
    It does not determine whether the need is real.
    """

    errors: List[str] = []

    if not isinstance(analysis, dict):
        return {
            "valid": False,
            "errors": ["Analysis must be a dictionary."],
            "status": "INVALID",
        }

    need = analysis.get("need", {})

    if not isinstance(need, dict):
        errors.append("Need structure is invalid.")
    else:
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

    if not isinstance(analysis, dict):
        return ""

    need = analysis.get("need", {})

    if not isinstance(need, dict):
        return ""

    return _normalize_text(
        need.get("statement")
    )


def _normalize_evidence(
    evidence: Any,
) -> List[Any]:
    """
    Normalize evidence into a list.

    This function does not assign evidentiary validity.
    Evidence quality is evaluated later by Reality Gate.
    """

    if evidence is None:
        return []

    if isinstance(evidence, list):
        return evidence

    if isinstance(evidence, dict):
        items = evidence.get("items")

        if isinstance(items, list):
            return items

        return [evidence]

    return [evidence]


def _extract_explicit_need(
    evidence: List[Any],
) -> Dict[str, Any] | None:
    """
    Search supplied evidence for an explicitly structured need.

    Accepted forms include:

        {"need": {"statement": "..."}}

    or:

        {"need": "..."}

    or directly:

        {"statement": "...", "type": "..."}
    """

    for item in evidence:
        if not isinstance(item, dict):
            continue

        candidate = item.get("need")

        if isinstance(candidate, dict):
            if candidate.get("statement"):
                return candidate

        if isinstance(candidate, str):
            if candidate.strip():
                return {
                    "statement": candidate.strip(),
                }

        if item.get("statement"):
            return item

    return None


def _build_need_from_evidence(
    candidate: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Normalize an explicitly supplied need candidate.
    """

    return {
        "statement": _normalize_text(
            candidate.get("statement")
        ),
        "type": _normalize_need_type(
            candidate.get("type")
        ),
        "area": _normalize_text(
            candidate.get("area")
        ),
        "function": _normalize_text(
            candidate.get("function")
        ),
        "process": _normalize_text(
            candidate.get("process")
        ),
        "activity": _normalize_text(
            candidate.get("activity")
        ),
        "task": _normalize_text(
            candidate.get("task")
        ),
        "actor": _normalize_text(
            candidate.get("actor")
        ),
    }


def _build_need_hypothesis(
    *,
    objective: str,
) -> str:
    """
    Construct a provisional need hypothesis from the stated objective.

    The wording deliberately identifies it as a requirement rather
    than claiming that a specific problem has already been proven.
    """

    return (
        f"The business requires a condition or capability that "
        f"supports the objective: {objective}"
    )


def _normalize_need_type(
    value: Any,
) -> str | None:
    """
    Normalize a supplied need type.

    Unknown or absent types remain None rather than being invented.
    """

    normalized = _normalize_text(value).lower()

    if normalized in NEED_TYPES:
        return normalized

    return None


def _normalize_text(
    value: Any,
) -> str:
    """
    Convert a value to normalized text without failing when API
    contracts provide non-string values.
    """

    if value is None:
        return ""

    return str(value).strip()