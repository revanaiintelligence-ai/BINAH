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