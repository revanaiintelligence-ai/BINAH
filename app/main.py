from fastapi import FastAPI

from app.models import AnalyzeRequest, AnalyzeResponse, RealityGateRequest
from app.core import analyze, diagnose_capability, reality_gate


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