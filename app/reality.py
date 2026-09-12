from typing import Any, Dict, List


REALITY_GATE_STATUS = [
    "VALIDATED",
    "STOP_NEED_NOT_VALIDATED",
]


REALITY_GATE_CRITERIA = [
    "need_exists",
    "sufficient_evidence",
    "relevant_consequences",
    "exists_currently",
    "desired_by_business",
    "capability_insufficient",
]


def evaluate_reality_gate(
    *,
    need: Dict[str, Any],
    evidence: List[Dict[str, Any]] | None = None,
    relevant_consequences: Any = None,
    exists_currently: bool | None = None,
    desired_by_business: bool | None = None,
    capability_insufficient: bool | None = None,
) -> Dict[str, Any]:
    """
    Evaluate whether a business need has sufficient reality
    and evidence to proceed with deeper analysis.

    BINAH principle:
    Reality before Analysis.

    The Reality Gate does not select a solution and does not
    determine whether AI should be used.
    """

    normalized_evidence = evidence or []

    need_exists = _need_exists(need)
    sufficient_evidence = len(normalized_evidence) > 0
    consequences_present = _value_exists(relevant_consequences)

    criteria = {
        "need_exists": need_exists,
        "sufficient_evidence": sufficient_evidence,
        "relevant_consequences": consequences_present,
        "exists_currently": exists_currently is True,
        "desired_by_business": desired_by_business is True,
        "capability_insufficient": capability_insufficient is True,
    }

    validated = all(criteria.values())

    if validated:
        status = "VALIDATED"
        conclusion = (
            "The need passes the Reality Gate and can proceed "
            "to second-level decomposition and alternative evaluation."
        )
        next_action = (
            "Proceed to second decomposition of the affected "
            "area, process, activity, and task."
        )
    else:
        status = "STOP_NEED_NOT_VALIDATED"
        failed_criteria = [
            criterion
            for criterion, passed in criteria.items()
            if not passed
        ]

        conclusion = (
            "The need does not currently satisfy the Reality Gate. "
            "Analysis must stop until the failed criteria are resolved."
        )

        next_action = (
            "Investigate and resolve the failed Reality Gate criteria: "
            + ", ".join(failed_criteria)
            + "."
        )

    return {
        "status": status,
        "validated": validated,
        "criteria": criteria,
        "need": need,
        "evidence": normalized_evidence,
        "conclusion": conclusion,
        "next_action": next_action,
    }


def validate_reality_gate(
    gate_result: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Validate the structural integrity of a Reality Gate result.
    """

    required_fields = [
        "status",
        "validated",
        "criteria",
        "need",
        "evidence",
        "conclusion",
        "next_action",
    ]

    missing_fields = [
        field
        for field in required_fields
        if field not in gate_result
    ]

    status_valid = gate_result.get("status") in REALITY_GATE_STATUS
    validated_consistent = (
        gate_result.get("validated") is True
        and gate_result.get("status") == "VALIDATED"
    ) or (
        gate_result.get("validated") is False
        and gate_result.get("status") == "STOP_NEED_NOT_VALIDATED"
    )

    return {
        "valid": (
            len(missing_fields) == 0
            and status_valid
            and validated_consistent
        ),
        "missing_fields": missing_fields,
        "status_valid": status_valid,
        "validated_consistent": validated_consistent,
    }


def _need_exists(need: Dict[str, Any]) -> bool:
    """
    Determine whether a usable need definition exists.
    """

    if not isinstance(need, dict):
        return False

    statement = need.get("statement")

    if isinstance(statement, str):
        return bool(statement.strip())

    return _value_exists(statement)


def _value_exists(value: Any) -> bool:
    """
    Determine whether a required value contains usable information.
    """

    if value is None:
        return False

    if isinstance(value, str):
        return bool(value.strip())

    if isinstance(value, (list, tuple, set, dict)):
        return len(value) > 0

    return True