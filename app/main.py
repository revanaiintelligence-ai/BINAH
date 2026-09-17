"""
BINAH — API Layer

HTTP/API layer for BINAH v0.2.

This module is responsible only for:
- API application configuration
- HTTP routes
- request validation through Pydantic models
- translating API contracts into module contracts
- delegation to BINAH analytical modules

Business methodology and analytical logic remain outside this layer.
"""

from fastapi import FastAPI

from app.models import (
    AnalyzeRequest,
    AnalyzeResponse,
    BusinessDecompositionRequest,
    NeedIdentificationRequest,
    CapabilityDiagnosisRequest,
    RealityGateRequest,
    TaskDecompositionRequest,
    AlternativesEvaluationRequest,
    SolutionEvaluationRequest,
    AIEvaluationRequest,
    WorkDesignRequest,
    AgentSpecificationRequest,
    OpportunityIdentificationRequest,
    DiagnosticGenerationRequest,
)

from app.orchestrator import run_binah_analysis
from app.business import decompose_business
from app.needs import identify_need
from app.capability import diagnose_capability
from app.reality import evaluate_reality_gate
from app.tasks import decompose_need_tasks
from app.alternatives import evaluate_alternatives
from app.solutions import evaluate_solutions
from app.ai import evaluate_ai
from app.work import design_work
from app.agents import specify_agent
from app.opportunities import identify_opportunities
from app.diagnostic import generate_diagnostic


BINAH_VERSION = "0.2"


app = FastAPI(
    title="BINAH API",
    description=(
        "BINAH — Business Intelligence & Need Analysis Hunters. "
        "Business, process, task, need, capability, solution, "
        "AI, work, opportunity, and diagnostic analysis."
    ),
    version=BINAH_VERSION,
)


@app.get("/")
def root():
    """Return basic API information."""
    return {
        "name": "BINAH API",
        "methodology": "BINAH",
        "version": BINAH_VERSION,
        "status": "operational",
    }


@app.get("/health")
def health():
    """Return API health status."""
    return {
        "status": "ok",
        "version": BINAH_VERSION,
    }


@app.post(
    "/v1/binah/analyze",
    response_model=AnalyzeResponse,
)
def analyze_endpoint(request: AnalyzeRequest):
    """Execute the complete BINAH analytical workflow."""

    result = run_binah_analysis(
        business=request.business,
        context=request.context,
        objective=request.objective,
        evidence=request.evidence,
    )

    if isinstance(result, dict):
        result.setdefault("methodology", "BINAH")
        result.setdefault("version", BINAH_VERSION)
        result.setdefault("business", request.business)
        result.setdefault("context", request.context)
        result.setdefault("objective", request.objective)

        # Public API contract uses `trace`.
        # Internal orchestrator uses `traceability`.
        if "trace" not in result and "traceability" in result:
            result["trace"] = result["traceability"]

    return result


@app.post("/v1/business/decompose")
def business_decompose_endpoint(
    request: BusinessDecompositionRequest,
):
    """Perform the initial business decomposition."""

    return decompose_business(
        business=request.business,
        context=request.context,
    )


@app.post("/v1/needs/identify")
def needs_identify_endpoint(
    request: NeedIdentificationRequest,
):
    """Identify and structure the business need."""

    business_map = decompose_business(
        business=request.business,
        context=request.context,
    )

    return identify_need(
        business=request.business,
        context=request.context,
        objective=request.objective,
        business_map=business_map,
        evidence=request.evidence,
    )


@app.post("/v1/capability/diagnose")
def capability_diagnose_endpoint(
    request: CapabilityDiagnosisRequest,
):
    """Diagnose required capability, current capability, and gap."""

    return diagnose_capability(
        need=request.need,
        business_map=request.business_map,
    )


@app.post("/v1/gates/reality")
def reality_gate_endpoint(
    request: RealityGateRequest,
):
    """Evaluate whether the need passes the Reality Gate."""

    return evaluate_reality_gate(
        need=request.need,
        evidence=request.evidence,
        relevant_consequences=request.consequences,
        exists_currently=request.exists,
        desired_by_business=request.wants_to_solve,
        capability_insufficient=request.capability_insufficient,
    )


@app.post("/v1/tasks/decompose")
def tasks_decompose_endpoint(
    request: TaskDecompositionRequest,
):
    """
    Perform the second-level task decomposition.

    The current tasks.py contract accepts only:
    need, business_map, and reality_gate.
    Detailed task variables are populated later through
    tasks.py functions such as define_task().
    """

    return decompose_need_tasks(
        need=request.need,
        business_map=request.business_map,
        reality_gate=request.reality_gate,
    )


@app.post("/v1/alternatives/evaluate")
def alternatives_evaluate_endpoint(
    request: AlternativesEvaluationRequest,
):
    """
    Prepare the available alternatives for evaluation.

    The current alternatives.py contract accepts:
    need and second_decomposition.
    """

    return evaluate_alternatives(
        need=request.need,
        second_decomposition=request.second_decomposition,
    )


@app.post("/v1/solutions/evaluate")
def solutions_evaluate_endpoint(
    request: SolutionEvaluationRequest,
):
    """Prepare and evaluate candidate solutions."""

    return evaluate_solutions(
        need=request.need,
        alternatives=request.alternatives,
    )


@app.post("/v1/ai/evaluate")
def ai_evaluate_endpoint(
    request: AIEvaluationRequest,
):
    """Evaluate whether and how AI should participate."""

    return evaluate_ai(
        need=request.need,
        task=request.task,
        alternatives=request.alternatives,
        solution_evaluation=request.solution_evaluation,
    )


@app.post("/v1/work/design")
def work_design_endpoint(
    request: WorkDesignRequest,
):
    """Design the required work structure."""

    return design_work(
        need=request.need,
        second_decomposition=request.second_decomposition,
        ai_evaluation=request.ai_evaluation,
    )


@app.post("/v1/agents/specify")
def agents_specify_endpoint(
    request: AgentSpecificationRequest,
):
    """Specify a specialized agent only when justified."""

    return specify_agent(
        need=request.need,
        ai_evaluation=request.ai_evaluation,
        work_design=request.work_design,
        solution_evaluation=request.solution_evaluation,
    )


@app.post("/v1/opportunities/identify")
def opportunities_identify_endpoint(
    request: OpportunityIdentificationRequest,
):
    """Identify business opportunities from the analysis."""

    return identify_opportunities(
        need=request.need,
        solution_evaluation=request.solution_evaluation,
        ai_evaluation=request.ai_evaluation,
        work_design=request.work_design,
        agent_specification=request.agent_specification,
    )


@app.post("/v1/diagnostic/generate")
def diagnostic_generate_endpoint(
    request: DiagnosticGenerationRequest,
):
    """Generate the final BINAH diagnostic."""

    return generate_diagnostic(
        business=request.business,
        context=request.context,
        objective=request.objective,
        need=request.need,
        capability=request.capability,
        gap=request.gap,
        reality_gate=request.reality_gate,
        alternatives=request.alternatives,
        solution_evaluation=request.solution_evaluation,
        ai_evaluation=request.ai_evaluation,
        work_design=request.work_design,
        agent_specification=request.agent_specification,
        opportunities=request.opportunities,
    )