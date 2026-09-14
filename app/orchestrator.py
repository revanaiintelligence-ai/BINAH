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

    BINAH follows the principle:

        Need before AI.

    The orchestrator coordinates the analytical modules but does not
    implement their methodology. Each module remains responsible for
    its own domain logic.

    Flow:

        Business
        → Need
        → Capability
        → Reality Gate
        → Second Decomposition
        → Alternatives
        → Solutions
        → AI
        → Work / Agent
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

    if not _reality_gate_validated(reality_gate):
        result["status"] = "STOP_NEED_NOT_VALIDATED"

        diagnostic = generate_diagnostic(
            business=business,
            context=context,
            objective=objective,
            need=need,
            capability=capability_result,
            gap=result["gap"],
            reality_gate=reality_gate,
            alternatives=None,
            solution_evaluation=None,
            ai_evaluation=None,
            work_design=None,
            agent_specification=None,
            opportunities=None,
        )

        result["diagnostic"] = diagnostic
        result["status"] = diagnostic.get(
            "status",
            "STOP_NEED_NOT_VALIDATED",
        )

        add_trace_stage(
            trace,
            stage="finding",
            data=diagnostic,
        )

        return result

    # ---------------------------------------------------------
    # 5. SECOND DECOMPOSITION
    # ---------------------------------------------------------

    second_decomposition = decompose_need_tasks(
        need=need,
        business_map=business_map,
        reality_gate=reality_gate,
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

    result["status"] = diagnostic.get(
        "status",
        "ANALYSIS_COMPLETE",
    )

    return result


def _run_reality_gate(
    *,
    need: Any,
    evidence: Any,
    capability: Any,
) -> Dict[str, Any]:
    """
    Translate upstream analysis into the explicit Reality Gate
    criteria required by the reality module.
    """

    exists = _extract_boolean(
        need,
        "exists",
        default=True,
    )

    wants_to_solve = _extract_boolean(
        need,
        "wants_to_solve",
        default=True,
    )

    capability_insufficient = _extract_capability_insufficient(
        capability
    )

    consequences = _extract_value(
        need,
        "consequences",
        default=None,
    )

    return evaluate_reality_gate(
        need=need,
        evidence=evidence,
        consequences=consequences,
        exists=exists,
        wants_to_solve=wants_to_solve,
        capability_insufficient=capability_insufficient,
    )


def _reality_gate_validated(
    reality_gate: Any,
) -> bool:
    """
    Determine whether the Reality Gate authorizes continuation.
    """

    if not isinstance(reality_gate, dict):
        return False

    status = reality_gate.get("status")

    if status == "VALIDATED":
        return True

    if reality_gate.get("validated") is True:
        return True

    if reality_gate.get("passes") is True:
        return True

    return False


def _extract_capability_insufficient(
    capability: Any,
) -> bool:
    """
    Extract whether current capability is insufficient relative
    to required capability.
    """

    if not isinstance(capability, dict):
        return False

    if capability.get("capability_insufficient") is True:
        return True

    if capability.get("insufficient") is True:
        return True

    status = capability.get("status")

    return status in {
        "INSUFFICIENT",
        "PARTIALLY_SUFFICIENT",
    }


def _extract_boolean(
    source: Any,
    key: str,
    *,
    default: bool,
) -> bool:
    """
    Safely extract a boolean value from a module result.
    """

    if isinstance(source, dict):
        value = source.get(key)

        if isinstance(value, bool):
            return value

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