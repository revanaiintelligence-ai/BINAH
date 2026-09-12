from typing import Any, Dict

from app.traceability import create_trace


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
    Execute the BINAH methodology in its defined sequence.

    BINAH principle:
    Need before AI.

    The orchestrator coordinates the methodology.
    Each specialized module remains responsible for its own logic.
    """

    trace = create_trace(
        input_data={
            "business": business,
            "context": context,
            "objective": objective,
        },
        observation=None,
        evidence=evidence,
        analysis=None,
        reasoning=None,
        finding=None,
        recommendation=None,
    )

    result = {
        "methodology": "BINAH",
        "version": BINAH_VERSION,
        "status": "IN_PROGRESS",
        "business": business,
        "context": context,
        "objective": objective,
        "trace": trace,
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
        "result": None,
    }

    # ---------------------------------------------------------
    # PHASE 1 — BUSINESS UNDERSTANDING
    # ---------------------------------------------------------

    result["business_map"] = _run_business_decomposition(
        business=business,
        context=context,
    )

    # ---------------------------------------------------------
    # PHASE 2 — NEED DISCOVERY
    # ---------------------------------------------------------

    result["need"] = _run_need_identification(
        business=business,
        context=context,
        objective=objective,
        business_map=result["business_map"],
        evidence=evidence,
    )

    # ---------------------------------------------------------
    # PHASE 3 — CAPABILITY DIAGNOSIS
    # ---------------------------------------------------------

    result["capability"] = _run_capability_diagnosis(
        need=result["need"],
        business_map=result["business_map"],
    )

    result["gap"] = result["capability"].get("gap")

    # ---------------------------------------------------------
    # PHASE 4 — REALITY GATE
    # ---------------------------------------------------------

    result["reality_gate"] = _run_reality_gate(
        need=result["need"],
        evidence=evidence,
        capability=result["capability"],
    )

    if not result["reality_gate"].get("validated", False):
        result["status"] = "STOPPED"
        result["result"] = "STOP_NEED_NOT_VALIDATED"

        result["diagnostic"] = _run_diagnostic(
            result=result,
        )

        return result

    # ---------------------------------------------------------
    # PHASE 5 — SECOND DECOMPOSITION
    # ---------------------------------------------------------

    result["second_decomposition"] = _run_task_decomposition(
        need=result["need"],
        business_map=result["business_map"],
    )

    # ---------------------------------------------------------
    # PHASE 6 — ALTERNATIVES BEFORE AI
    # ---------------------------------------------------------

    result["alternatives"] = _run_alternatives_evaluation(
        need=result["need"],
        second_decomposition=result["second_decomposition"],
    )

    # ---------------------------------------------------------
    # PHASE 7 — SOLUTION EVALUATION
    # ---------------------------------------------------------

    result["solution_evaluation"] = _run_solution_evaluation(
        need=result["need"],
        alternatives=result["alternatives"],
        second_decomposition=result["second_decomposition"],
    )

    # ---------------------------------------------------------
    # PHASE 8 — AI GATE
    # ---------------------------------------------------------

    result["ai_evaluation"] = _run_ai_evaluation(
        need=result["need"],
        second_decomposition=result["second_decomposition"],
        alternatives=result["alternatives"],
        solution_evaluation=result["solution_evaluation"],
    )

    ai_result = result["ai_evaluation"].get("result")

    # ---------------------------------------------------------
    # PHASE 9 — WORK DESIGN
    # ---------------------------------------------------------

    if ai_result in {
        "AI_NOT_JUSTIFIED",
        "AI_INAPPROPRIATE",
        "NON_AI_SOLUTION_RECOMMENDED",
        "PROCESS_IMPROVEMENT_RECOMMENDED",
        "SOFTWARE_RECOMMENDED",
        "TRADITIONAL_AUTOMATION_RECOMMENDED",
    }:
        result["work_design"] = _run_work_design(
            need=result["need"],
            second_decomposition=result["second_decomposition"],
            solution_evaluation=result["solution_evaluation"],
        )

    # ---------------------------------------------------------
    # PHASE 10 — AGENT SPECIFICATION
    # ---------------------------------------------------------

    if ai_result in {
        "AI_USEFUL",
        "AI_AUGMENTED",
        "AI_RECOMMENDED",
        "HYBRID_SOLUTION_RECOMMENDED",
    }:
        result["agent_specification"] = _run_agent_specification(
            need=result["need"],
            second_decomposition=result["second_decomposition"],
            ai_evaluation=result["ai_evaluation"],
        )

    # ---------------------------------------------------------
    # PHASE 11 — OPPORTUNITY IDENTIFICATION
    # ---------------------------------------------------------

    result["opportunities"] = _run_opportunity_identification(
        result=result,
    )

    # ---------------------------------------------------------
    # PHASE 12 — FINAL DIAGNOSTIC
    # ---------------------------------------------------------

    result["diagnostic"] = _run_diagnostic(
        result=result,
    )

    result["status"] = "COMPLETED"

    return result


# =============================================================
# MODULE COORDINATION
# =============================================================


def _run_business_decomposition(
    *,
    business: str,
    context: str,
) -> Dict[str, Any]:

    from app.business import decompose_business

    return decompose_business(
        business=business,
        context=context,
    )


def _run_need_identification(
    *,
    business: str,
    context: str,
    objective: str,
    business_map: Dict[str, Any],
    evidence: Any,
) -> Dict[str, Any]:

    from app.needs import identify_need

    return identify_need(
        business=business,
        context=context,
        objective=objective,
        business_map=business_map,
        evidence=evidence,
    )


def _run_capability_diagnosis(
    *,
    need: Dict[str, Any],
    business_map: Dict[str, Any],
) -> Dict[str, Any]:

    from app.capability import diagnose_capability

    return diagnose_capability(
        need=need,
        business_map=business_map,
    )


def _run_reality_gate(
    *,
    need: Dict[str, Any],
    evidence: Any,
    capability: Dict[str, Any],
) -> Dict[str, Any]:

    from app.reality import evaluate_reality_gate

    return evaluate_reality_gate(
        need=need,
        evidence=evidence,
        capability=capability,
    )


def _run_task_decomposition(
    *,
    need: Dict[str, Any],
    business_map: Dict[str, Any],
) -> Dict[str, Any]:

    from app.tasks import decompose_need_tasks

    return decompose_need_tasks(
        need=need,
        business_map=business_map,
    )


def _run_alternatives_evaluation(
    *,
    need: Dict[str, Any],
    second_decomposition: Dict[str, Any],
) -> Dict[str, Any]:

    from app.alternatives import evaluate_alternatives

    return evaluate_alternatives(
        need=need,
        task_decomposition=second_decomposition,
    )


def _run_solution_evaluation(
    *,
    need: Dict[str, Any],
    alternatives: Dict[str, Any],
    second_decomposition: Dict[str, Any],
) -> Dict[str, Any]:

    from app.solutions import evaluate_solutions

    return evaluate_solutions(
        need=need,
        alternatives=alternatives,
        task_decomposition=second_decomposition,
    )


def _run_ai_evaluation(
    *,
    need: Dict[str, Any],
    second_decomposition: Dict[str, Any],
    alternatives: Dict[str, Any],
    solution_evaluation: Dict[str, Any],
) -> Dict[str, Any]:

    from app.ai import evaluate_ai

    return evaluate_ai(
        need=need,
        task_decomposition=second_decomposition,
        alternatives=alternatives,
        solution_evaluation=solution_evaluation,
    )


def _run_work_design(
    *,
    need: Dict[str, Any],
    second_decomposition: Dict[str, Any],
    solution_evaluation: Dict[str, Any],
) -> Dict[str, Any]:

    from app.work import design_work

    return design_work(
        need=need,
        task_decomposition=second_decomposition,
        solution_evaluation=solution_evaluation,
    )


def _run_agent_specification(
    *,
    need: Dict[str, Any],
    second_decomposition: Dict[str, Any],
    ai_evaluation: Dict[str, Any],
) -> Dict[str, Any]:

    from app.agents import specify_agent

    return specify_agent(
        need=need,
        task_decomposition=second_decomposition,
        ai_evaluation=ai_evaluation,
    )


def _run_opportunity_identification(
    *,
    result: Dict[str, Any],
) -> Dict[str, Any]:

    from app.opportunities import identify_opportunities

    return identify_opportunities(
        analysis=result,
    )


def _run_diagnostic(
    *,
    result: Dict[str, Any],
) -> Dict[str, Any]:

    from app.diagnostic import generate_diagnostic

    return generate_diagnostic(
        analysis=result,
    )