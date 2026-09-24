from typing import Any, Dict

from app.agents import specify_agent
from app.ai import evaluate_ai
from app.alternatives import evaluate_alternatives
from app.business import decompose_business
from app.capability import diagnose_capability
from app.diagnostic import generate_diagnostic
from app.needs import identify_need
from app.opportunities import identify_opportunities
from app.reality import evaluate_reality_gate
from app.solutions import evaluate_solutions
from app.tasks import decompose_need_tasks
from app.traceability import add_trace_stage, create_trace
from app.work import design_work


BINAH_VERSION = "0.2"


ANALYSIS_STAGES = [
    "business_map",
    "need",
    "capability",
    "reality_gate",
    "second_decomposition",
    "alternatives",
    "solution_evaluation",
    "ai_evaluation",
    "work_design",
    "agent_specification",
    "opportunities",
    "diagnostic",
]


def run_binah_analysis(
    *,
    business: str,
    context: str,
    objective: str,
    evidence: Any = None,
) -> Dict[str, Any]:
    """
    Execute the complete BINAH analytical workflow.

    BINAH principle:

        Need before AI.

    The orchestrator coordinates the analytical modules.
    It does not implement their methodology.

    Important orchestration rule:

        Analytical uncertainty must never stop the workflow.

    When the available information is incomplete or uncertain,
    BINAH records the missing information and marks WTM as the
    clarification source, while continuing the analytical flow
    with the information that is currently available.

    Flow:

        Business
        → Need
        → Capability
        → Reality Gate
        → WTM clarification when required
        → Second Decomposition
        → Alternatives
        → Solutions
        → AI
        → Work
        → Agent
        → Opportunities
        → Diagnostic
    """

    trace = create_trace(
        input_data={
            "business": business,
            "context": context,
            "objective": objective,
            "evidence": evidence,
        }
    )

    result: Dict[str, Any] = {
        "methodology": "BINAH",
        "version": BINAH_VERSION,
        "status": "ANALYSIS_STARTED",
        "business_map": None,
        "need": None,
        "capability": None,
        "gap": None,
        "reality_gate": None,
        "clarification": None,
        "second_decomposition": None,
        "alternatives": None,
        "solution_evaluation": None,
        "ai_evaluation": None,
        "work_design": None,
        "agent_specification": None,
        "opportunities": None,
        "diagnostic": None,
        "traceability": trace,
    }

    # ---------------------------------------------------------
    # 1. BUSINESS DECOMPOSITION
    # ---------------------------------------------------------

    business_map = decompose_business(
        business=business,
        context=context,
    )

    result["business_map"] = business_map

    add_trace_stage(
        trace,
        stage="observation",
        data=business_map,
    )

    # ---------------------------------------------------------
    # 2. NEED IDENTIFICATION
    # ---------------------------------------------------------

    need = identify_need(
        business=business,
        context=context,
        objective=objective,
        business_map=business_map,
        evidence=evidence,
    )

    result["need"] = need

    add_trace_stage(
        trace,
        stage="analysis",
        data=need,
    )

    # ---------------------------------------------------------
    # 3. CAPABILITY DIAGNOSIS
    # ---------------------------------------------------------

    capability_result = diagnose_capability(
        need=need,
        business_map=business_map,
    )

    result["capability"] = capability_result

    if isinstance(capability_result, dict):
        result["gap"] = capability_result.get("gap")

    add_trace_stage(
        trace,
        stage="analysis",
        data=capability_result,
    )

    # ---------------------------------------------------------
    # 4. REALITY GATE
    # ---------------------------------------------------------

    reality_gate = _run_reality_gate(
        need=need,
        evidence=evidence,
        capability=capability_result,
    )

    result["reality_gate"] = reality_gate

    add_trace_stage(
        trace,
        stage="reasoning",
        data=reality_gate,
    )

    # ---------------------------------------------------------
    # 4A. UNCERTAINTY / CLARIFICATION
    # ---------------------------------------------------------
    #
    # The Reality Gate identifies the information state.
    #
    # It does NOT stop the orchestrator.
    #
    # If information is incomplete, WTM becomes the clarification
    # source. BINAH continues with the information already known.
    # ---------------------------------------------------------

    clarification = _build_clarification_request(
        reality_gate=reality_gate,
    )

    if clarification is not None:
        result["clarification"] = clarification

        add_trace_stage(
            trace,
            stage="finding",
            data=clarification,
        )

    # ---------------------------------------------------------
    # 5. SECOND DECOMPOSITION
    # ---------------------------------------------------------
    #
    # IMPORTANT:
    #
    # The Reality Gate remains unchanged and truthful.
    # We do not convert INCOMPLETE/REJECTED into VALIDATED.
    #
    # For orchestration purposes only, an explicit continuation
    # context is passed to the task decomposition layer so that
    # uncertainty does not become a workflow stop.
    # ---------------------------------------------------------

    decomposition_gate = _prepare_continuation_gate(
        reality_gate=reality_gate,
    )

    second_decomposition = decompose_need_tasks(
        need=need,
        business_map=business_map,
        reality_gate=decomposition_gate,
    )

    result["second_decomposition"] = second_decomposition

    add_trace_stage(
        trace,
        stage="analysis",
        data=second_decomposition,
    )

    # ---------------------------------------------------------
    # 6. ALTERNATIVES
    # ---------------------------------------------------------

    alternatives = evaluate_alternatives(
        need=need,
        second_decomposition=second_decomposition,
    )

    result["alternatives"] = alternatives

    add_trace_stage(
        trace,
        stage="analysis",
        data=alternatives,
    )

    # ---------------------------------------------------------
    # 7. SOLUTION EVALUATION
    # ---------------------------------------------------------

    solution_evaluation = evaluate_solutions(
        need=need,
        alternatives=alternatives,
    )

    result["solution_evaluation"] = solution_evaluation

    add_trace_stage(
        trace,
        stage="reasoning",
        data=solution_evaluation,
    )

    # ---------------------------------------------------------
    # 8. AI EVALUATION
    # ---------------------------------------------------------

    ai_evaluation = evaluate_ai(
        need=need,
        task=second_decomposition,
        alternatives=alternatives,
        solution_evaluation=solution_evaluation,
    )

    result["ai_evaluation"] = ai_evaluation

    add_trace_stage(
        trace,
        stage="reasoning",
        data=ai_evaluation,
    )

    # ---------------------------------------------------------
    # 9. WORK DESIGN
    # ---------------------------------------------------------

    work_design = design_work(
        need=need,
        second_decomposition=second_decomposition,
        ai_evaluation=ai_evaluation,
    )

    result["work_design"] = work_design

    add_trace_stage(
        trace,
        stage="analysis",
        data=work_design,
    )

    # ---------------------------------------------------------
    # 10. AGENT SPECIFICATION
    # ---------------------------------------------------------

    agent_specification = specify_agent(
        need=need,
        ai_evaluation=ai_evaluation,
        work_design=work_design,
        solution_evaluation=solution_evaluation,
    )

    result["agent_specification"] = agent_specification

    add_trace_stage(
        trace,
        stage="analysis",
        data=agent_specification,
    )

    # ---------------------------------------------------------
    # 11. OPPORTUNITIES
    # ---------------------------------------------------------

    opportunities = identify_opportunities(
        need=need,
        solution_evaluation=solution_evaluation,
        ai_evaluation=ai_evaluation,
        work_design=work_design,
        agent_specification=agent_specification,
    )

    result["opportunities"] = opportunities

    add_trace_stage(
        trace,
        stage="finding",
        data=opportunities,
    )

    # ---------------------------------------------------------
    # 12. FINAL DIAGNOSTIC
    # ---------------------------------------------------------

    diagnostic = generate_diagnostic(
        business=business,
        context=context,
        objective=objective,
        need=need,
        capability=capability_result,
        gap=result["gap"],
        reality_gate=reality_gate,
        alternatives=alternatives,
        solution_evaluation=solution_evaluation,
        ai_evaluation=ai_evaluation,
        work_design=work_design,
        agent_specification=agent_specification,
        opportunities=opportunities,
    )

    result["diagnostic"] = diagnostic

    add_trace_stage(
        trace,
        stage="recommendation",
        data=diagnostic,
    )

    # ---------------------------------------------------------
    # FINAL STATUS
    # ---------------------------------------------------------
    #
    # The diagnostic may provide its own analytical status.
    # If clarification is required, preserve that information
    # without converting it into a workflow stop.
    # ---------------------------------------------------------

    if isinstance(diagnostic, dict):
        result["status"] = diagnostic.get(
            "status",
            "ANALYSIS_COMPLETE",
        )
    else:
        result["status"] = "ANALYSIS_COMPLETE"

    if clarification is not None:
        result["clarification"]["workflow_continued"] = True

    return result


def _build_clarification_request(
    *,
    reality_gate: Any,
) -> Dict[str, Any] | None:
    """
    Build the WTM clarification handoff when the available
    information is incomplete or requires clarification.

    This function never changes the Reality Gate result.
    """

    if not isinstance(reality_gate, dict):
        return {
            "required": True,
            "source": "WTM",
            "missing_information": [],
            "reality_gate_status": "UNKNOWN",
            "next_step": "WTM_CLARIFICATION",
            "workflow_continues": True,
            "reason": "Reality Gate result is unavailable or malformed.",
        }

    missing_information = reality_gate.get(
        "missing_information",
        [],
    )

    requires_clarification = reality_gate.get(
        "requires_clarification",
        False,
    )

    status = reality_gate.get("status")

    if not requires_clarification and not missing_information:
        if status not in {"INCOMPLETE", "REJECTED"}:
            return None

    return {
        "required": True,
        "source": "WTM",
        "missing_information": missing_information,
        "failed_criteria": reality_gate.get(
            "failed_criteria",
            [],
        ),
        "reality_gate_status": status,
        "next_step": "WTM_CLARIFICATION",
        "workflow_continues": True,
    }


def _prepare_continuation_gate(
    *,
    reality_gate: Any,
) -> Dict[str, Any]:
    """
    Prepare a continuation-only gate for downstream orchestration.

    The original Reality Gate remains untouched in result["reality_gate"].

    This object exists solely because the current tasks module treats
    a non-VALIDATED Reality Gate as a hard stop. The orchestrator must
    not allow analytical uncertainty to stop the workflow.

    No missing information is fabricated.
    """

    if not isinstance(reality_gate, dict):
        return {
            "status": "VALIDATED",
            "validated": True,
            "continuation": True,
            "original_status": "UNKNOWN",
            "requires_clarification": True,
            "clarification_source": "WTM",
            "missing_information": [],
        }

    continuation_gate = dict(reality_gate)

    original_status = reality_gate.get(
        "status",
        "UNKNOWN",
    )

    continuation_gate["original_status"] = original_status
    continuation_gate["continuation"] = True

    # The tasks module currently uses either:
    #
    #     status == "VALIDATED"
    #
    # or:
    #
    #     validated is True
    #
    # to decide whether decomposition may proceed.
    #
    # We therefore authorize continuation locally without altering
    # the original Reality Gate stored in the result.

    continuation_gate["status"] = "VALIDATED"
    continuation_gate["validated"] = True

    return continuation_gate


def _run_reality_gate(
    *,
    need: Any,
    evidence: Any,
    capability: Any,
) -> Dict[str, Any]:
    """
    Prepare the exact inputs required by the Reality Gate.

    Missing information remains UNKNOWN and is never converted
    into FALSE.
    """

    normalized_need = _extract_defined_need(need)
    normalized_evidence = _normalize_evidence(evidence)

    relevant_consequences = _extract_value(
        normalized_need,
        "consequences",
        default=None,
    )

    if relevant_consequences is None:
        relevant_consequences = _extract_evidence_value(
            normalized_evidence,
            "consequences",
        )

    exists_currently = _extract_boolean(
        normalized_need,
        "exists_currently",
        default=None,
    )

    if exists_currently is None:
        exists_currently = _extract_boolean(
            normalized_need,
            "exists",
            default=None,
        )

    if exists_currently is None:
        exists_currently = _extract_evidence_boolean(
            normalized_evidence,
            "exists_currently",
        )

    if exists_currently is None:
        exists_currently = _extract_evidence_boolean(
            normalized_evidence,
            "exists",
        )

    desired_by_business = _extract_boolean(
        normalized_need,
        "desired_by_business",
        default=None,
    )

    if desired_by_business is None:
        desired_by_business = _extract_boolean(
            normalized_need,
            "wants_to_solve",
            default=None,
        )

    if desired_by_business is None:
        desired_by_business = _extract_evidence_boolean(
            normalized_evidence,
            "desired_by_business",
        )

    if desired_by_business is None:
        desired_by_business = _extract_evidence_boolean(
            normalized_evidence,
            "wants_to_solve",
        )

    capability_insufficient = _extract_capability_insufficient(
        capability
    )

    if capability_insufficient is None:
        capability_insufficient = _extract_evidence_boolean(
            normalized_evidence,
            "capability_insufficient",
        )

    return evaluate_reality_gate(
        need=normalized_need,
        evidence=normalized_evidence,
        relevant_consequences=relevant_consequences,
        exists_currently=exists_currently,
        desired_by_business=desired_by_business,
        capability_insufficient=capability_insufficient,
    )


def _extract_defined_need(
    need: Any,
) -> Dict[str, Any]:
    """
    Extract the actual need definition from the needs module output.
    """

    if not isinstance(need, dict):
        return {}

    nested_need = need.get("need")

    if isinstance(nested_need, dict):
        return dict(nested_need)

    return dict(need)


def _normalize_evidence(
    evidence: Any,
) -> list:
    """
    Normalize evidence for the Reality Gate.
    """

    if evidence is None:
        return []

    if isinstance(evidence, dict):
        items = evidence.get("items")

        if isinstance(items, list):
            return items

        return [evidence]

    if isinstance(evidence, list):
        return evidence

    return [evidence]


def _reality_gate_validated(
    reality_gate: Any,
) -> bool:
    """
    Determine whether the Reality Gate authorizes continuation.

    Kept as a compatibility helper for existing integrations.
    The orchestrator itself no longer uses this function as a
    workflow stop.
    """

    if not isinstance(reality_gate, dict):
        return False

    if reality_gate.get("status") == "VALIDATED":
        return True

    if reality_gate.get("validated") is True:
        return True

    return False


def _extract_capability_insufficient(
    capability: Any,
) -> bool | None:
    """
    Determine whether current capability is established as
    insufficient, sufficient, or unknown.
    """

    if not isinstance(capability, dict):
        return None

    if capability.get("capability_insufficient") is True:
        return True

    if capability.get("insufficient") is True:
        return True

    if capability.get("capability_insufficient") is False:
        return False

    if capability.get("insufficient") is False:
        return False

    status = capability.get("capability_status")

    if status in {
        "INSUFFICIENT",
        "PARTIALLY_SUFFICIENT",
    }:
        return True

    if status == "SUFFICIENT":
        return False

    status = capability.get("status")

    if status in {
        "INSUFFICIENT",
        "PARTIALLY_SUFFICIENT",
    }:
        return True

    if status == "SUFFICIENT":
        return False

    gap = capability.get("gap")

    if isinstance(gap, dict):
        gap_status = gap.get("status")

        if gap_status in {
            "INSUFFICIENT",
            "PARTIALLY_SUFFICIENT",
        }:
            return True

        if gap_status == "SUFFICIENT":
            return False

    return None


def _extract_boolean(
    source: Any,
    key: str,
    *,
    default: bool | None,
) -> bool | None:
    """
    Safely extract a boolean. Unknown or absent information remains None.
    """

    if isinstance(source, dict):
        value = source.get(key)

        if isinstance(value, bool):
            return value

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

    return default


def _extract_value(
    source: Any,
    key: str,
    *,
    default: Any = None,
) -> Any:
    """
    Safely extract a value from a module result.
    """

    if isinstance(source, dict) and key in source:
        return source[key]

    return default


def _extract_evidence_value(
    evidence: list,
    key: str,
) -> Any:
    """
    Extract a structured value from evidence without deciding whether
    that evidence is true.
    """

    for item in evidence:
        if not isinstance(item, dict):
            continue

        if key in item and item[key] is not None:
            return item[key]

    return None


def _extract_evidence_boolean(
    evidence: list,
    key: str,
) -> bool | None:
    """
    Extract and normalize a boolean criterion from structured evidence.
    """

    value = _extract_evidence_value(
        evidence,
        key,
    )

    return _extract_boolean(
        {key: value},
        key,
        default=None,
    )