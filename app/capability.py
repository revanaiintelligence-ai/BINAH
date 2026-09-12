from typing import Any, Dict


CAPABILITY_STATUS = [
    "SUFFICIENT",
    "PARTIALLY_SUFFICIENT",
    "INSUFFICIENT",
    "UNKNOWN",
]


def diagnose_capability(
    *,
    need: Dict[str, Any],
    business_map: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Diagnose the capability required to satisfy a business need.

    BINAH sequence:

    Need
        ↓
    Required Capability
        ↓
    Current Capability
        ↓
    Gap

    Formula:

    Required Capability - Current Capability = Gap

    This module does not evaluate solutions or AI.
    """

    need_data = _extract_need(need)

    return {
        "status": "CAPABILITY_DIAGNOSIS_READY",
        "need": need_data,
        "required_capability": None,
        "current_capability": None,
        "gap": None,
        "capability_status": "UNKNOWN",
        "evidence": [],
        "diagnosis": {
            "required": None,
            "current": None,
            "gap": None,
        },
        "business_map_available": bool(business_map),
    }


def define_capability(
    diagnosis: Dict[str, Any],
    *,
    required: str,
    current: str,
) -> Dict[str, Any]:
    """
    Define the required and current capabilities.
    """

    required_capability = required.strip()
    current_capability = current.strip()

    if not required_capability:
        raise ValueError(
            "Required capability is required."
        )

    if not current_capability:
        raise ValueError(
            "Current capability is required."
        )

    updated = dict(diagnosis)

    updated["required_capability"] = required_capability
    updated["current_capability"] = current_capability

    updated["diagnosis"] = {
        "required": required_capability,
        "current": current_capability,
        "gap": None,
    }

    updated["status"] = "READY_FOR_GAP_ANALYSIS"

    return updated


def calculate_gap(
    diagnosis: Dict[str, Any],
    *,
    gap: str,
    status: str = "INSUFFICIENT",
) -> Dict[str, Any]:
    """
    Record the capability gap identified between the required
    and current capability.
    """

    normalized_gap = gap.strip()
    normalized_status = status.strip().upper()

    if not normalized_gap:
        raise ValueError("Capability gap is required.")

    if normalized_status not in CAPABILITY_STATUS:
        raise ValueError(
            f"Invalid capability status: {status}"
        )

    updated = dict(diagnosis)

    updated["gap"] = normalized_gap
    updated["capability_status"] = normalized_status

    updated["diagnosis"] = {
        "required": updated.get("required_capability"),
        "current": updated.get("current_capability"),
        "gap": normalized_gap,
    }

    updated["status"] = "CAPABILITY_DIAGNOSED"

    return updated


def assess_capability(
    *,
    required: str,
    current: str,
    gap: str,
) -> Dict[str, Any]:
    """
    Create a complete capability diagnosis from the three
    explicit components:

    Required Capability
    Current Capability
    Gap
    """

    required_capability = required.strip()
    current_capability = current.strip()
    capability_gap = gap.strip()

    if not required_capability:
        raise ValueError(
            "Required capability is required."
        )

    if not current_capability:
        raise ValueError(
            "Current capability is required."
        )

    if not capability_gap:
        raise ValueError(
            "Capability gap is required."
        )

    status = (
        "SUFFICIENT"
        if capability_gap.lower() in {
            "none",
            "no gap",
            "no_gap",
        }
        else "INSUFFICIENT"
    )

    return {
        "status": "CAPABILITY_DIAGNOSED",
        "required_capability": required_capability,
        "current_capability": current_capability,
        "gap": capability_gap,
        "capability_status": status,
        "diagnosis": {
            "required": required_capability,
            "current": current_capability,
            "gap": capability_gap,
        },
    }


def validate_capability(
    diagnosis: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Validate the structural completeness of a capability diagnosis.
    """

    errors = []

    if not diagnosis.get("required_capability"):
        errors.append(
            "Required capability is missing."
        )

    if not diagnosis.get("current_capability"):
        errors.append(
            "Current capability is missing."
        )

    if not diagnosis.get("gap"):
        errors.append(
            "Capability gap is missing."
        )

    capability_status = diagnosis.get(
        "capability_status"
    )

    if capability_status not in CAPABILITY_STATUS:
        errors.append(
            "Capability status is invalid or missing."
        )

    return {
        "valid": not errors,
        "errors": errors,
        "status": (
            "VALID"
            if not errors
            else "INVALID"
        ),
    }


def _extract_need(
    need: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Extract the normalized need information without modifying it.
    """

    if not isinstance(need, dict):
        raise ValueError(
            "Need must be a dictionary."
        )

    nested_need = need.get("need")

    if isinstance(nested_need, dict):
        return dict(nested_need)

    return dict(need)