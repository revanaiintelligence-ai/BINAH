from fastapi import FastAPI

from app.models import AnalyzeRequest, AnalyzeResponse
from app.core import analyze


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