from typing import Any, Dict, List


TRACE_STAGES = [
    "input",
    "observation",
    "evidence",
    "analysis",
    "reasoning",
    "finding",
    "recommendation",
]


def create_trace(
    *,
    input_data: Any = None,
    observation: Any = None,
    evidence: Any = None,
    analysis: Any = None,
    reasoning: Any = None,
    finding: Any = None,
    recommendation: Any = None,
) -> Dict[str, Any]:
    """
    Create a standardized BINAH traceability structure.

    Flow:
    Input → Observation → Evidence → Analysis → Reasoning
    → Finding → Recommendation
    """

    return {
        "input": input_data,
        "observation": observation,
        "evidence": evidence,
        "analysis": analysis,
        "reasoning": reasoning,
        "finding": finding,
        "recommendation": recommendation,
    }


def validate_trace(trace: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate the basic structure of a BINAH trace.
    """

    missing_stages: List[str] = [
        stage
        for stage in TRACE_STAGES
        if stage not in trace
    ]

    return {
        "valid": len(missing_stages) == 0,
        "missing_stages": missing_stages,
    }


def add_trace_stage(
    trace: Dict[str, Any],
    stage: str,
    value: Any = None,
    *,
    data: Any = None,
) -> Dict[str, Any]:
    """
    Add or update a traceability stage.

    `value` is the canonical parameter.

    `data` is accepted as a compatibility alias because
    existing BINAH orchestration code may use `data=`.
    """

    if stage not in TRACE_STAGES:
        raise ValueError(
            f"Invalid traceability stage: {stage}"
        )

    if value is not None and data is not None:
        raise ValueError(
            "Provide either 'value' or 'data', not both."
        )

    stage_value = value if value is not None else data

    trace[stage] = stage_value

    return trace