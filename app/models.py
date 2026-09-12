from pydantic import BaseModel, Field
from typing import List, Optional


class AnalyzeRequest(BaseModel):
    problem: str = Field(..., min_length=1)
    business_context: Optional[str] = None
    current_process: Optional[str] = None
    desired_outcome: Optional[str] = None
    constraints: List[str] = []


class AnalyzeResponse(BaseModel):
    problem: str
    diagnosis: str
    need: str
    gap: str
    alternatives: List[str]
    ai_relevance: str
    next_action: str


class RealityGateRequest(BaseModel):
    need: str = Field(..., min_length=1)
    evidence: List[dict] = []
    relevant_consequences: str = Field(..., min_length=1)
    exists_currently: bool
    desired_by_business: bool
    capability_insufficient: bool


class TaskDecompositionRequest(BaseModel):
    need: str = Field(..., min_length=1)
    area: str = Field(..., min_length=1)
    function: str = Field(..., min_length=1)
    process: str = Field(..., min_length=1)
    activity: str = Field(..., min_length=1)
    task: str = Field(..., min_length=1)
    actor: str = Field(..., min_length=1)
    frequency: Optional[str] = None
    time_required: Optional[str] = None
    volume: Optional[str] = None
    input_data: Optional[str] = None
    decision: Optional[str] = None
    complexity: Optional[str] = None
    errors: Optional[str] = None
    dependency: Optional[str] = None
    repetition: Optional[str] = None
    bottleneck: Optional[str] = None


class AlternativesEvaluationRequest(BaseModel):
    need: str = Field(..., min_length=1)
    alternatives: List[str] = Field(..., min_length=1)


class AIEvaluationRequest(BaseModel):
    need: str = Field(..., min_length=1)
    task: str = Field(..., min_length=1)
    alternatives: List[str] = Field(..., min_length=1)