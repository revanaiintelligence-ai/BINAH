"""
BINAH — Shared API Models

Definitive request and response contracts for BINAH v0.2.

This module contains data contracts only.
Business methodology and analytical logic belong to the app modules.
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):
    """Request for the complete BINAH analysis."""

    business: Any = Field(
        ...,
        description="Business or organizational context being analyzed.",
    )

    context: Any = Field(
        ...,
        description="Relevant business context.",
    )

    objective: Any = Field(
        ...,
        description="Desired business result or objective.",
    )

    evidence: Optional[Any] = Field(
        default=None,
        description="Available evidence supporting the analysis.",
    )


class AnalyzeResponse(BaseModel):
    """Response from the complete BINAH analysis."""

    methodology: str = "BINAH"
    version: str = "0.2"
    status: str

    business: Any = None
    context: Any = None
    objective: Any = None

    trace: Optional[Dict[str, Any]] = None

    business_map: Optional[Dict[str, Any]] = None
    need: Optional[Dict[str, Any]] = None
    capability: Optional[Dict[str, Any]] = None
    gap: Any = None
    reality_gate: Optional[Dict[str, Any]] = None

    second_decomposition: Optional[Dict[str, Any]] = None
    alternatives: Optional[Dict[str, Any]] = None
    solution_evaluation: Optional[Dict[str, Any]] = None
    ai_evaluation: Optional[Dict[str, Any]] = None
    work_design: Optional[Dict[str, Any]] = None
    agent_specification: Optional[Dict[str, Any]] = None
    opportunities: Optional[Dict[str, Any]] = None
    diagnostic: Optional[Dict[str, Any]] = None

    result: Any = None


class BusinessDecompositionRequest(BaseModel):
    """Request for initial business decomposition."""

    business: Any = Field(
        ...,
        description="Business or organization to be decomposed.",
    )

    context: Optional[Any] = Field(
        default=None,
        description="Relevant context required to understand the business.",
    )


class NeedIdentificationRequest(BaseModel):
    """Request for identifying the real business need."""

    business: Any = Field(
        ...,
        description="Business or organizational context being analyzed.",
    )

    objective: Any = Field(
        ...,
        description="Desired business result or objective.",
    )

    context: Optional[Any] = Field(
        default=None,
        description="Relevant business context.",
    )

    evidence: Optional[Any] = Field(
        default=None,
        description="Available evidence supporting need identification.",
    )


class CapabilityDiagnosisRequest(BaseModel):
    """Request for capability diagnosis."""

    need: Any

    business_map: Optional[Dict[str, Any]] = None


class RealityGateRequest(BaseModel):
    """Request for Reality Gate evaluation."""

    need: Any

    evidence: Any = None

    consequences: Any = None

    exists: Optional[bool] = None

    wants_to_solve: Optional[bool] = None

    capability_insufficient: Optional[bool] = None


class TaskDecompositionRequest(BaseModel):
    """Request for second-level task decomposition."""

    need: Any

    business_map: Optional[Dict[str, Any]] = None

    reality_gate: Optional[Dict[str, Any]] = None

    area: Optional[str] = None

    function: Optional[str] = None

    process: Optional[str] = None

    activity: Optional[str] = None

    task: Optional[str] = None

    actor: Optional[str] = None

    frequency: Optional[str] = None

    time: Optional[Any] = None

    volume: Optional[Any] = None

    input_data: Optional[Any] = None

    information: Optional[Any] = None

    documents: Optional[Any] = None

    decision: Optional[Any] = None

    complexity: Optional[Any] = None

    errors: Optional[Any] = None

    dependency: Optional[Any] = None

    human_role: Optional[Any] = None

    repetition: Optional[Any] = None

    bottleneck: Optional[Any] = None

    efficiency: Optional[Any] = None

    improvement: Optional[Any] = None


class AlternativesEvaluationRequest(BaseModel):
    """Request for comparative alternative evaluation."""

    need: Any

    second_decomposition: Optional[Dict[str, Any]] = None

    alternatives: Optional[List[Dict[str, Any]]] = None


class SolutionEvaluationRequest(BaseModel):
    """Request for solution evaluation."""

    need: Any

    alternatives: Optional[Dict[str, Any]] = None


class AIEvaluationRequest(BaseModel):
    """Request for AI evaluation."""

    need: Any

    task: Optional[Any] = None

    alternatives: Optional[Any] = None

    solution_evaluation: Optional[Dict[str, Any]] = None


class WorkDesignRequest(BaseModel):
    """Request for work design."""

    need: Any

    second_decomposition: Optional[Dict[str, Any]] = None

    ai_evaluation: Optional[Dict[str, Any]] = None


class AgentSpecificationRequest(BaseModel):
    """Request for specialized agent specification."""

    need: Any

    ai_evaluation: Optional[Dict[str, Any]] = None

    work_design: Optional[Dict[str, Any]] = None

    solution_evaluation: Optional[Dict[str, Any]] = None


class OpportunityIdentificationRequest(BaseModel):
    """Request for opportunity identification."""

    need: Any

    solution_evaluation: Optional[Dict[str, Any]] = None

    ai_evaluation: Optional[Dict[str, Any]] = None

    work_design: Optional[Dict[str, Any]] = None

    agent_specification: Optional[Dict[str, Any]] = None


class DiagnosticGenerationRequest(BaseModel):
    """Request for final diagnostic generation."""

    business: Any

    context: Any

    objective: Any

    need: Any

    capability: Optional[Dict[str, Any]] = None

    gap: Any = None

    reality_gate: Optional[Dict[str, Any]] = None

    alternatives: Optional[Dict[str, Any]] = None

    solution_evaluation: Optional[Dict[str, Any]] = None

    ai_evaluation: Optional[Dict[str, Any]] = None

    work_design: Optional[Dict[str, Any]] = None

    agent_specification: Optional[Dict[str, Any]] = None

    opportunities: Optional[Dict[str, Any]] = None