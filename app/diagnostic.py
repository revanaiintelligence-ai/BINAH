"""
BINAH — Diagnostic Consolidation

Consolidates the complete BINAH analysis into a final diagnostic.

This module does not execute solutions, AI systems, or agents.
It produces an auditable conclusion based on the results of the
previous analytical stages.
"""

from typing import Any, Dict, List, Optional


DIAGNOSTIC_STATUSES = [
    "DIAGNOSTIC_READY",
    "DIAGNOSTIC_INCOMPLETE",
    "STOP_NEED_NOT_VALIDATED",
]

DIAGNOSTIC_RESULT_TYPES = [
    "NEED_NOT_VALIDATED",
    "CAPABILITY_SUFFICIENT",
    "PROCESS_IMPROVEMENT",
    "SOFTWARE_SOLUTION",
    "TRADITIONAL_AUTOMATION",
    "AI_NOW",
    "AI_LATER",
    "AI_PREPARATION",
    "AI_NOT_JUSTIFIED",
    "AI_INAPPROPRIATE",
    "HYBRID_SOLUTION",
    "MULTIPLE_OPPORTUNITIES",
]


def generate_diagnostic(
    *,
    business: Any,
    context: Any,
    objective: Any,
    need: Any,
    capability: Optional[Dict[str, Any]] = None,
    gap: Any = None,
    reality_gate: Optional[Dict[str, Any]] = None,
    alternatives: Optional[Dict[str, Any]] = None,
    solution_evaluation: Optional[Dict[str, Any]] = None,
    ai_evaluation: Optional[Dict[str, Any]] = None,
    work_design: Optional[Dict[str, Any]] = None,
    agent_specification: Optional[Dict[str, Any]] = None,
    opportunities: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Consolidate the complete BINAH analysis into a final diagnostic.

    The diagnostic preserves the distinction between:
        observation
        evidence
        analysis
        finding
        recommendation

    No diagnostic is considered valid if the Reality Gate failed.
    """

    normalized_need = _normalize_text_or_structure(need)

    if not normalized_need:
        return _stop_diagnostic(
            reason="No validated need is available."
        )

    gate = reality_gate or {}

    if gate.get("validated") is False:
        return _stop_diagnostic(
            reason=(
                "Reality Gate did not validate the business need."
            ),
            reality_gate=gate,
        )

    if not gate:
        return {
            "status": "DIAGNOSTIC_INCOMPLETE",
            "result_type": "NEED_NOT_VALIDATED",
            "business": business,
            "context": context,
            "objective": objective,
            "need": normalized_need,
            "finding": (
                "Reality Gate evidence is required before a final "
                "diagnostic can be issued."
            ),
            "recommendation": (
                "Complete Reality Gate evaluation."
            ),
            "validation": {
                "valid": False,
                "errors": [
                    "Reality Gate result is missing."
                ],
            },
        }

    capability_result = capability or {}
    alternatives_result = alternatives or {}
    solutions_result = solution_evaluation or {}
    ai_result = ai_evaluation or {}
    work_result = work_design or {}
    agent_result = agent_specification or {}
    opportunity_result = opportunities or {}

    finding = build_finding(
        need=normalized_need,
        capability=capability_result,
        gap=gap,
        reality_gate=gate,
        alternatives=alternatives_result,
        solution_evaluation=solutions_result,
        ai_evaluation=ai_result,
        work_design=work_result,
        agent_specification=agent_result,
        opportunities=opportunity_result,
    )

    result_type = determine_diagnostic_result(
        capability=capability_result,
        solution_evaluation=solutions_result,
        ai_evaluation=ai_result,
        opportunities=opportunity_result,
    )

    recommendation = build_recommendation(
        result_type=result_type,
        solution_evaluation=solutions_result,
        ai_evaluation=ai_result,
        work_design=work_result,
        agent_specification=agent_result,
        opportunities=opportunity_result,
    )

    conclusion = build_conclusion(
        need=normalized_need,
        result_type=result_type,
        finding=finding,
        recommendation=recommendation,
    )

    return {
        "status": "DIAGNOSTIC_READY",
        "result_type": result_type,
        "business": business,
        "context": context,
        "objective": objective,
        "need": normalized_need,
        "capability": capability_result,
        "gap": gap,
        "reality_gate": gate,
        "finding": finding,
        "recommendation": recommendation,
        "conclusion": conclusion,
        "ai_summary": build_ai_summary(ai_result),
        "work_summary": build_work_summary(work_result),
        "agent_summary": build_agent_summary(agent_result),
        "opportunity_summary": build_opportunity_summary(
            opportunity_result
        ),
        "traceability": build_diagnostic_traceability(
            need=normalized_need,
            reality_gate=gate,
            capability=capability_result,
            solution_evaluation=solutions_result,
            ai_evaluation=ai_result,
            opportunities=opportunity_result,
        ),
        "validation": validate_diagnostic(
            {
                "status": "DIAGNOSTIC_READY",
                "result_type": result_type,
                "need": normalized_need,
                "finding": finding,
                "recommendation": recommendation,
                "conclusion": conclusion,
            }
        ),
    }


def determine_diagnostic_result(
    *,
    capability: Optional[Dict[str, Any]] = None,
    solution_evaluation: Optional[Dict[str, Any]] = None,
    ai_evaluation: Optional[Dict[str, Any]] = None,
    opportunities: Optional[Dict[str, Any]] = None,
) -> str:
    """
    Determine the principal diagnostic result.

    AI is not automatically the result.
    The result follows the complete analysis.
    """

    capability_result = capability or {}
    solutions = solution_evaluation or {}
    ai = ai_evaluation or {}
    opportunity_result = opportunities or {}

    capability_status = capability_result.get("status")

    if capability_status == "SUFFICIENT":
        return "CAPABILITY_SUFFICIENT"

    ai_outcome = ai.get("outcome")

    if ai_outcome == "AI_NOW":
        if _has_non_ai_hybrid_signal(solutions):
            return "HYBRID_SOLUTION"

        return "AI_NOW"

    if ai_outcome == "AI_LATER":
        return "AI_LATER"

    if ai_outcome == "AI_PREPARATION":
        return "AI_PREPARATION"

    if ai_outcome == "AI_NOT_JUSTIFIED":
        return "AI_NOT_JUSTIFIED"

    if ai_outcome == "AI_INAPPROPRIATE":
        return "AI_INAPPROPRIATE"

    result_type = _extract_solution_result_type(
        solutions
    )

    solution_mapping = {
        "PROCESS_IMPROVEMENT_RECOMMENDED": (
            "PROCESS_IMPROVEMENT"
        ),
        "SOFTWARE_RECOMMENDED": "SOFTWARE_SOLUTION",
        "TRADITIONAL_AUTOMATION_RECOMMENDED": (
            "TRADITIONAL_AUTOMATION"
        ),
        "HYBRID_SOLUTION_RECOMMENDED": (
            "HYBRID_SOLUTION"
        ),
    }

    if result_type in solution_mapping:
        return solution_mapping[result_type]

    opportunity_list = opportunity_result.get(
        "opportunities",
        [],
    )

    if isinstance(opportunity_list, list) and len(
        opportunity_list
    ) > 1:
        return "MULTIPLE_OPPORTUNITIES"

    return "MULTIPLE_OPPORTUNITIES"


def build_finding(
    *,
    need: str,
    capability: Dict[str, Any],
    gap: Any,
    reality_gate: Dict[str, Any],
    alternatives: Dict[str, Any],
    solution_evaluation: Dict[str, Any],
    ai_evaluation: Dict[str, Any],
    work_design: Dict[str, Any],
    agent_specification: Dict[str, Any],
    opportunities: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Build the principal analytical finding.
    """

    capability_status = capability.get(
        "status",
        capability.get("capability_status"),
    )

    ai_outcome = ai_evaluation.get("outcome")

    return {
        "need": need,
        "need_validated": bool(
            reality_gate.get("validated")
        ),
        "capability_status": capability_status,
        "gap": gap,
        "ai_outcome": ai_outcome,
        "agent_justified": (
            agent_specification.get("status")
            == "SPECIFIED"
        ),
        "opportunity_count": _count_opportunities(
            opportunities
        ),
        "statement": _build_finding_statement(
            need=need,
            capability_status=capability_status,
            ai_outcome=ai_outcome,
        ),
    }


def build_recommendation(
    *,
    result_type: str,
    solution_evaluation: Dict[str, Any],
    ai_evaluation: Dict[str, Any],
    work_design: Dict[str, Any],
    agent_specification: Dict[str, Any],
    opportunities: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Build an actionable recommendation from the final result.
    """

    ai = ai_evaluation or {}
    solutions = solution_evaluation or {}
    work = work_design or {}
    agents = agent_specification or {}
    opportunity_result = opportunities or {}

    if result_type == "CAPABILITY_SUFFICIENT":
        return {
            "type": "MAINTAIN",
            "action": (
                "Maintain the current capability and monitor "
                "the relevant business condition."
            ),
        }

    if result_type == "AI_NOW":
        return {
            "type": "AI",
            "action": (
                ai.get("recommendation")
                or "Evaluate implementation of the justified AI opportunity."
            ),
            "human_role": ai.get("human_role"),
            "application_type": ai.get(
                "recommended_application_type"
            ),
        }

    if result_type == "AI_LATER":
        return {
            "type": "AI_LATER",
            "action": (
                "Do not force AI adoption now. Preserve and develop "
                "the conditions required for a future AI application."
            ),
            "preparation_plan": ai.get(
                "preparation_plan",
                [],
            ),
        }

    if result_type == "AI_PREPARATION":
        return {
            "type": "AI_PREPARATION",
            "action": (
                "Prepare the business for future AI adoption by "
                "closing identified readiness gaps."
            ),
            "preparation_plan": ai.get(
                "preparation_plan",
                [],
            ),
            "readiness_gaps": ai.get(
                "readiness_gaps",
                [],
            ),
        }

    if result_type == "AI_NOT_JUSTIFIED":
        return {
            "type": "NON_AI_FIRST",
            "action": (
                "Do not implement AI for the current need. "
                "Use the justified non-AI solution while preserving "
                "the identified future AI path where applicable."
            ),
        }

    if result_type == "AI_INAPPROPRIATE":
        return {
            "type": "AVOID_AI",
            "action": (
                "Do not use AI for this need because the analysis "
                "indicates that AI is inappropriate."
            ),
        }

    if result_type == "HYBRID_SOLUTION":
        return {
            "type": "HYBRID",
            "action": (
                _extract_solution_recommendation(
                    solutions
                )
                or "Implement a hybrid human and technology solution."
            ),
            "human_role": ai.get("human_role"),
        }

    if result_type == "PROCESS_IMPROVEMENT":
        return {
            "type": "PROCESS",
            "action": (
                _extract_solution_recommendation(
                    solutions
                )
                or "Redesign the relevant process."
            ),
            "work_design": work,
        }

    if result_type == "SOFTWARE_SOLUTION":
        return {
            "type": "SOFTWARE",
            "action": (
                _extract_solution_recommendation(
                    solutions
                )
                or "Evaluate the recommended software solution."
            ),
        }

    if result_type == "TRADITIONAL_AUTOMATION":
        return {
            "type": "TRADITIONAL_AUTOMATION",
            "action": (
                _extract_solution_recommendation(
                    solutions
                )
                or "Evaluate traditional automation."
            ),
        }

    if result_type == "MULTIPLE_OPPORTUNITIES":
        return {
            "type": "OPPORTUNITY_PORTFOLIO",
            "action": (
                "Prioritize the identified opportunities before "
                "selecting implementation."
            ),
            "priority_order": opportunity_result.get(
                "priority_order",
                [],
            ),
        }

    return {
        "type": "REVIEW",
        "action": (
            "Review the complete analysis before implementation."
        ),
    }


def build_conclusion(
    *,
    need: str,
    result_type: str,
    finding: Dict[str, Any],
    recommendation: Dict[str, Any],
) -> str:
    """
    Produce the final concise diagnostic conclusion.
    """

    recommendation_action = recommendation.get(
        "action",
        "Review the analysis.",
    )

    result_labels = {
        "CAPABILITY_SUFFICIENT": (
            "The current capability is sufficient."
        ),
        "PROCESS_IMPROVEMENT": (
            "The principal opportunity is process improvement."
        ),
        "SOFTWARE_SOLUTION": (
            "The principal opportunity is a software solution."
        ),
        "TRADITIONAL_AUTOMATION": (
            "The principal opportunity is traditional automation."
        ),
        "AI_NOW": (
            "AI has a currently justified application."
        ),
        "AI_LATER": (
            "AI may become useful later, but immediate adoption "
            "is not the appropriate conclusion."
        ),
        "AI_PREPARATION": (
            "The business should prepare for future AI adoption."
        ),
        "AI_NOT_JUSTIFIED": (
            "AI is not justified for the current need."
        ),
        "AI_INAPPROPRIATE": (
            "AI is inappropriate for the current need."
        ),
        "HYBRID_SOLUTION": (
            "A hybrid human and technology solution is indicated."
        ),
        "MULTIPLE_OPPORTUNITIES": (
            "Multiple actionable opportunities were identified."
        ),
    }

    label = result_labels.get(
        result_type,
        "The analysis requires further review.",
    )

    return (
        f"Need: {need}. "
        f"{label} "
        f"Recommended action: {recommendation_action}"
    )


def build_ai_summary(
    ai_evaluation: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Summarize AI findings without losing the distinction between
    now, later, and preparation.
    """

    ai = ai_evaluation or {}

    return {
        "outcome": ai.get("outcome"),
        "current_opportunities": ai.get(
            "current_opportunities",
            [],
        ),
        "future_opportunities": ai.get(
            "future_opportunities",
            [],
        ),
        "readiness_gaps": ai.get(
            "readiness_gaps",
            [],
        ),
        "preparation_plan": ai.get(
            "preparation_plan",
            [],
        ),
        "evolution_path": ai.get(
            "ai_evolution_path",
            [],
        ),
        "human_role": ai.get(
            "human_role"
        ),
        "recommended_application_type": ai.get(
            "recommended_application_type"
        ),
    }


def build_work_summary(
    work_design: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Summarize work-design implications.
    """

    work = work_design or {}

    return {
        "status": work.get("status"),
        "result_type": work.get("result_type"),
        "actions": work.get(
            "actions",
            [],
        ),
        "structure": work.get(
            "work_structure",
            work.get("structure"),
        ),
    }


def build_agent_summary(
    agent_specification: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Summarize agent architecture if it was justified.
    """

    agents = agent_specification or {}

    return {
        "status": agents.get("status"),
        "justification_result": agents.get(
            "justification_result"
        ),
        "agent_type": agents.get(
            "agent_type"
        ),
        "human_role": agents.get(
            "human_role"
        ),
        "specification_available": isinstance(
            agents.get("specification"),
            dict,
        ),
    }


def build_opportunity_summary(
    opportunities: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Summarize the Opportunity Map.
    """

    result = opportunities or {}

    return {
        "status": result.get("status"),
        "opportunity_count": result.get(
            "opportunity_count",
            0,
        ),
        "priority_order": result.get(
            "priority_order",
            [],
        ),
        "ai_opportunity_map": result.get(
            "ai_opportunity_map",
            {},
        ),
    }


def build_diagnostic_traceability(
    *,
    need: str,
    reality_gate: Dict[str, Any],
    capability: Dict[str, Any],
    solution_evaluation: Dict[str, Any],
    ai_evaluation: Dict[str, Any],
    opportunities: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Build a compact traceability chain for the final diagnostic.
    """

    return {
        "input": {
            "need": need,
        },
        "evidence": reality_gate.get(
            "evidence",
            [],
        ),
        "analysis": {
            "capability": capability,
            "solution_evaluation": solution_evaluation,
            "ai_evaluation": ai_evaluation,
        },
        "finding": {
            "ai_outcome": ai_evaluation.get(
                "outcome"
            ),
            "opportunities": opportunities.get(
                "opportunities",
                [],
            ),
        },
        "recommendation": {
            "priority_order": opportunities.get(
                "priority_order",
                [],
            ),
        },
    }


def validate_diagnostic(
    diagnostic: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Validate final diagnostic completeness.
    """

    if not isinstance(diagnostic, dict):
        return {
            "valid": False,
            "errors": [
                "Diagnostic must be a dictionary."
            ],
        }

    errors: List[str] = []

    if diagnostic.get("status") not in {
        "DIAGNOSTIC_READY",
        "DIAGNOSTIC_INCOMPLETE",
        "STOP_NEED_NOT_VALIDATED",
    }:
        errors.append(
            "Invalid diagnostic status."
        )

    if diagnostic.get("status") == "DIAGNOSTIC_READY":
        if not diagnostic.get("need"):
            errors.append(
                "A validated need is required."
            )

        if not diagnostic.get("finding"):
            errors.append(
                "A finding is required."
            )

        if not diagnostic.get("recommendation"):
            errors.append(
                "A recommendation is required."
            )

        if not diagnostic.get("conclusion"):
            errors.append(
                "A conclusion is required."
            )

    return {
        "valid": len(errors) == 0,
        "errors": errors,
    }


def get_diagnostic_conclusion(
    diagnostic: Dict[str, Any],
) -> Optional[str]:
    """
    Return the final diagnostic conclusion.
    """

    if not isinstance(diagnostic, dict):
        return None

    conclusion = diagnostic.get("conclusion")

    if isinstance(conclusion, str):
        return conclusion

    return None


def _stop_diagnostic(
    *,
    reason: str,
    reality_gate: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Standard stop result when the need is not validated.
    """

    return {
        "status": "STOP_NEED_NOT_VALIDATED",
        "result_type": "NEED_NOT_VALIDATED",
        "finding": {
            "statement": reason,
        },
        "recommendation": {
            "type": "STOP",
            "action": (
                "Do not proceed to solution selection. "
                "Return to need validation."
            ),
        },
        "conclusion": (
            "BINAH cannot issue a solution recommendation "
            "until the need is validated."
        ),
        "reality_gate": reality_gate or {},
        "validation": {
            "valid": True,
            "errors": [],
        },
    }


def _normalize_text_or_structure(
    value: Any,
) -> str:
    """
    Normalize a string or structured object into a need statement.
    """

    if isinstance(value, str):
        return value.strip()

    if isinstance(value, dict):
        for key in (
            "statement",
            "need",
            "description",
            "name",
        ):
            candidate = value.get(key)

            if isinstance(candidate, str) and candidate.strip():
                return candidate.strip()

    return ""


def _extract_solution_result_type(
    solution_evaluation: Dict[str, Any],
) -> Optional[str]:
    """
    Extract the selected solution result type.
    """

    recommended = solution_evaluation.get(
        "recommended_solution"
    )

    if isinstance(recommended, dict):
        result_type = recommended.get(
            "result_type"
        )

        if result_type:
            return result_type

    result_type = solution_evaluation.get(
        "result_type"
    )

    if isinstance(result_type, str):
        return result_type

    return None


def _extract_solution_recommendation(
    solution_evaluation: Dict[str, Any],
) -> Optional[str]:
    """
    Extract a recommendation from solution evaluation.
    """

    recommended = solution_evaluation.get(
        "recommended_solution"
    )

    if isinstance(recommended, dict):
        for key in (
            "recommendation",
            "description",
            "action",
        ):
            value = recommended.get(key)

            if isinstance(value, str) and value.strip():
                return value.strip()

    for key in (
        "recommendation",
        "action",
    ):
        value = solution_evaluation.get(key)

        if isinstance(value, str) and value.strip():
            return value.strip()

    return None


def _count_opportunities(
    opportunities: Dict[str, Any],
) -> int:
    """
    Count identified opportunities.
    """

    values = opportunities.get(
        "opportunities",
        [],
    )

    if isinstance(values, list):
        return len(values)

    return 0


def _build_finding_statement(
    *,
    need: str,
    capability_status: Any,
    ai_outcome: Any,
) -> str:
    """
    Construct a concise finding statement.
    """

    capability_text = (
        str(capability_status)
        if capability_status
        else "UNKNOWN"
    )

    ai_text = (
        str(ai_outcome)
        if ai_outcome
        else "NOT_DETERMINED"
    )

    return (
        f"The validated need is '{need}'. "
        f"Current capability status: {capability_text}. "
        f"AI assessment: {ai_text}."
    )


def _has_non_ai_hybrid_signal(
    solution_evaluation: Dict[str, Any],
) -> bool:
    """
    Detect whether solution evaluation indicates a hybrid solution.
    """

    result_type = _extract_solution_result_type(
        solution_evaluation
    )

    return result_type == "HYBRID_SOLUTION_RECOMMENDED"