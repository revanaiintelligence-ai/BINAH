"""
Tests for the WTM → BINAH integration adapter.

These tests verify that:
- WTM cases marked as ready can be converted to AnalyzeRequest.
- WTM cases not ready are rejected.
- Required WTM fields are validated.
- WTM evidence is serialized correctly.
- WTM situation is not silently discarded from the integration payload.
"""

import pytest
from pydantic import BaseModel

from app.models import AnalyzeRequest
from app.wtm_adapter import (
    WTMAdapter,
    WTMIntegrationError,
)


class FakeEvidence(BaseModel):
    """Minimal evidence model compatible with WTM evidence objects."""

    id: str
    content: str
    type: str
    source: str
    status: str


class FakeWTMOutput:
    """Minimal WTM output used to test the adapter contract."""

    def __init__(
        self,
        *,
        ready_for_binah=True,
        business="Empresa de ejemplo",
        context="Contexto empresarial de prueba",
        objective="Mejorar el proceso principal",
        situation="El proceso presenta demoras",
        evidence=None,
        blocking_reasons=None,
    ):
        self.ready_for_binah = ready_for_binah
        self.business = business
        self.context = context
        self.objective = objective
        self.situation = situation
        self.evidence = evidence or []
        self.blocking_reasons = blocking_reasons or []


def test_ready_wtm_output_creates_binah_request():
    """A ready WTM output must become a valid BINAH request."""

    wtm_output = FakeWTMOutput()

    request = WTMAdapter.to_binah_request(wtm_output)

    assert isinstance(request, AnalyzeRequest)
    assert request.business == wtm_output.business
    assert request.context == wtm_output.context
    assert request.objective == wtm_output.objective


def test_not_ready_wtm_output_is_rejected():
    """WTM must explicitly authorize the handoff to BINAH."""

    wtm_output = FakeWTMOutput(
        ready_for_binah=False,
        blocking_reasons=["Falta información del contexto."],
    )

    with pytest.raises(WTMIntegrationError) as error:
        WTMAdapter.to_binah_request(wtm_output)

    assert "WTM case is not ready for BINAH" in str(error.value)
    assert "Falta información del contexto." in str(error.value)


def test_not_ready_without_blocking_reasons_is_rejected():
    """A case without readiness must still be rejected."""

    wtm_output = FakeWTMOutput(
        ready_for_binah=False,
    )

    with pytest.raises(WTMIntegrationError) as error:
        WTMAdapter.to_binah_request(wtm_output)

    assert str(error.value) == "WTM case is not ready for BINAH."


def test_missing_business_is_rejected():
    """Business is required by the BINAH request contract."""

    wtm_output = FakeWTMOutput(
        business=None,
    )

    with pytest.raises(WTMIntegrationError) as error:
        WTMAdapter.to_binah_request(wtm_output)

    assert str(error.value) == "WTM output does not contain a business."


def test_missing_context_is_rejected():
    """Context is required by the BINAH request contract."""

    wtm_output = FakeWTMOutput(
        context=None,
    )

    with pytest.raises(WTMIntegrationError) as error:
        WTMAdapter.to_binah_request(wtm_output)

    assert str(error.value) == "WTM output does not contain context."


def test_missing_objective_is_rejected():
    """Objective is required by the BINAH request contract."""

    wtm_output = FakeWTMOutput(
        objective=None,
    )

    with pytest.raises(WTMIntegrationError) as error:
        WTMAdapter.to_binah_request(wtm_output)

    assert str(error.value) == "WTM output does not contain objective."


def test_wtm_evidence_is_serialized():
    """WTM evidence objects must become plain dictionaries."""

    evidence = [
        FakeEvidence(
            id="E_001",
            content="Los clientes esperan demasiado.",
            type="USER_STATEMENT",
            source="conversation:001",
            status="PROVISIONAL",
        )
    ]

    wtm_output = FakeWTMOutput(
        evidence=evidence,
    )

    request = WTMAdapter.to_binah_request(wtm_output)

    assert isinstance(request.evidence, list)
    assert len(request.evidence) == 1

    item = request.evidence[0]

    assert item["id"] == "E_001"
    assert item["content"] == "Los clientes esperan demasiado."
    assert item["type"] == "USER_STATEMENT"
    assert item["source"] == "conversation:001"
    assert item["status"] == "PROVISIONAL"


def test_dictionary_evidence_is_preserved():
    """Dictionary evidence must remain usable by the BINAH contract."""

    evidence = [
        {
            "id": "E_001",
            "content": "Evidence from external source.",
            "type": "OBSERVATION",
            "source": "external",
            "status": "PROVISIONAL",
        }
    ]

    wtm_output = FakeWTMOutput(
        evidence=evidence,
    )

    request = WTMAdapter.to_binah_request(wtm_output)

    assert request.evidence == evidence


def test_empty_evidence_becomes_empty_list():
    """No evidence must produce an empty evidence collection."""

    wtm_output = FakeWTMOutput(
        evidence=[],
    )

    request = WTMAdapter.to_binah_request(wtm_output)

    assert request.evidence == []


def test_situation_is_not_mistaken_for_binah_context():
    """
    WTM situation must not silently replace BINAH context.

    The current BINAH AnalyzeRequest has no dedicated situation field.
    This test protects the existing contract until the final integration
    treatment of WTM situation is explicitly defined.
    """

    wtm_output = FakeWTMOutput(
        context="Contexto real del negocio",
        situation="Situación específica del proceso",
    )

    request = WTMAdapter.to_binah_request(wtm_output)

    assert request.context == "Contexto real del negocio"
    assert request.context != wtm_output.situation


def test_adapter_preserves_business_context_and_objective():
    """The adapter must preserve WTM information without interpretation."""

    wtm_output = FakeWTMOutput(
        business="Clínica privada",
        context="Tiene tres áreas operativas.",
        objective="Reducir los tiempos de atención.",
    )

    request = WTMAdapter.to_binah_request(wtm_output)

    assert request.business == "Clínica privada"
    assert request.context == "Tiene tres áreas operativas."
    assert request.objective == "Reducir los tiempos de atención."


def test_adapter_accepts_plain_string_evidence():
    """Unexpected simple evidence values are converted safely to text."""

    wtm_output = FakeWTMOutput(
        evidence=[
            "Los trabajadores reportan retrasos.",
        ],
    )

    request = WTMAdapter.to_binah_request(wtm_output)

    assert request.evidence == [
        {
            "content": "Los trabajadores reportan retrasos.",
        }
    ]