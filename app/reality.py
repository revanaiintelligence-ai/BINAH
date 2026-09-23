"""
BINAH — Reality Gate

The Reality Gate determines whether BINAH has enough information
to continue its analytical workflow.

Important distinction:

    TRUE     = condition is established
    FALSE    = condition is contradicted / not satisfied
    UNKNOWN  = insufficient information to determine the condition

UNKNOWN must NOT be treated as FALSE.

When the Gate cannot validate because information is incomplete,
WTM may be invoked to clarify and structure the missing information.
"""

from typing import Any, Dict


REALITY_GATE_STATUS = [
    "VALIDATED",
    "INCOMPLETE",
    "REJECTED",
]


def evaluate_reality_gate(
    *,
    need: Dict[str, Any],
    evidence: list,
    relevant_consequences: Any,
    exists_currently: Any,
    desired_by_business: Any,
    capability_insufficient: Any,
) -> Dict[str, Any]:
    """
    Evaluate whether the available information is sufficient
    to validate the business need.

    Values may be:

        True
        False
        None / UNKNOWN

    None means that the information is not yet sufficient
    to determine the condition.

    The Gate must distinguish:

        FALSE  !=  UNKNOWN
    """

    criteria = {
        "need_exists": _evaluate_need_exists(need),
        "sufficient_evidence": _has_evidence(evidence),
        "relevant_consequences": _has_value(relevant_consequences),
        "exists_currently": _normalize_boolean(
            exists_currently
        ),
        "desired_by_business": _normalize_boolean(
            desired_by_business
        ),
        "capability_insufficient": _normalize_boolean(
            capability_insufficient
        ),
    }

    missing_information = [
        key
        for key, value in criteria.items()
        if value is None
    ]

    failed_criteria = [
        key
        for key, value in criteria.items()
        if value is False
    ]

    if failed_criteria:
        status = "REJECTED"
        validated = False

        reason = (
            "The Reality Gate rejected the need because one or "
            "more required conditions are not satisfied."
        )

    elif missing_information:
        status = "INCOMPLETE"
        validated = False

        reason = (
            "The Reality Gate cannot yet validate the need because "
            "required information is incomplete or unknown."
        )

    else:
        status = "VALIDATED"
        validated = True

        reason = (
            "All Reality Gate criteria have sufficient information "
            "and the need is authorized to continue."
        )

    return {
        "status": status,
        "validated": validated,

        "criteria": criteria,

        "missing_information": missing_information,

        "failed_criteria": failed_criteria,

        "requires_clarification": bool(
            missing_information
        ),

        "clarification_source": (
            "WTM"
            if missing_information
            else None
        ),

        "reason": reason,
    }


def _normalize_boolean(
    value: Any,
) -> bool | None:
    """
    Normalize boolean-like values.

    True  -> True
    False -> False
    None / unknown -> None

    Unknown information is deliberately preserved as UNKNOWN.
    """

    if isinstance(value, bool):
        return value

    if value is None:
        return None

    if isinstance(value, str):
        normalized = value.strip().lower()

        if normalized in {
            "true",
            "yes",
            "si",
            "sí",
            "confirmed",
            "validated",
        }:
            return True

        if normalized in {
            "false",
            "no",
            "not",
            "rejected",
            "contradicted",
        }:
            return False

        if normalized in {
            "unknown",
            "undefined",
            "incomplete",
            "pending",
            "not_known",
            "not_available",
        }:
            return None

    return None


def _evaluate_need_exists(
    need: Any,
) -> bool | None:
    """
    Determine whether a need statement is actually present.

    Missing information is UNKNOWN.
    """

    if not isinstance(need, dict):
        return None

    statement = need.get("statement")

    if statement is None:
        return None

    if isinstance(statement, str):
        if not statement.strip():
            return None

        return True

    return True


def _has_evidence(
    evidence: Any,
) -> bool | None:
    """
    Determine whether evidence has been supplied.

    No evidence is treated as UNKNOWN rather than FALSE because
    absence of supplied evidence does not prove that no evidence
    exists in reality.
    """

    if evidence is None:
        return None

    if isinstance(evidence, list):
        return True if len(evidence) > 0 else None

    if isinstance(evidence, dict):
        if not evidence:
            return None

        return True

    return True


def _has_value(
    value: Any,
) -> bool | None:
    """
    Determine whether a relevant consequence/value has been
    identified.

    Missing information remains UNKNOWN.
    """

    if value is None:
        return None

    if isinstance(value, str):
        return True if value.strip() else None

    if isinstance(value, list):
        return True if len(value) > 0 else None

    if isinstance(value, dict):
        return True if value else None

    return True