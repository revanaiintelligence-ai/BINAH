from fastapi import FastAPI

from app.models import (
    AnalyzeRequest,
    AnalyzeResponse,
    RealityGateRequest,
    TaskDecompositionRequest,
    AlternativesEvaluationRequest,
    AIEvaluationRequest,
)
from app.core import analyze, diagnose_capability, reality_gate
from app.tasks import decompose_task
from app.alternatives import evaluate_alternatives
from app.ai import evaluate_ai


app = FastAPI(
    title="BINAH API",
    description="Business Intelligence & Need Analysis Hunters API",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "name": "BINAH API",
        "version": "0.1.0",
        "status": "operational",
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze_endpoint(request: AnalyzeRequest):
    return analyze(request)


@app.post("/capability/diagnose")
def capability_diagnose_endpoint(
    need: str,
    current_capability: str,
    constraints: list[str] | None = None,
):
    return diagnose_capability(
        need=need,
        current_capability=current_capability,
        constraints=constraints,
    )


@app.post("/reality-gate")
def reality_gate_endpoint(request: RealityGateRequest):
    return reality_gate(request)


@app.post("/tasks/decompose")
def tasks_decompose_endpoint(request: TaskDecompositionRequest):
    return decompose_task(
        need=request.need,
        area=request.area,
        function=request.function,
        process=request.process,
        activity=request.activity,
        task=request.task,
        actor=request.actor,
        frequency=request.frequency,
        time_required=request.time_required,
        volume=request.volume,
        input_data=request.input_data,
        decision=request.decision,
        complexity=request.complexity,
        errors=request.errors,
        dependency=request.dependency,
        repetition=request.repetition,
        bottleneck=request.bottleneck,
    )


@app.post("/alternatives/evaluate")
def alternatives_evaluate_endpoint(
    request: AlternativesEvaluationRequest,
):
    return evaluate_alternatives(
        need=request.need,
        alternatives=request.alternatives,
    )


@app.post("/ai/evaluate")
def ai_evaluate_endpoint(
    request: AIEvaluationRequest,
):
    return evaluate_ai(
        need=request.need,
        task=request.task,
        alternatives=request.alternatives,
    )