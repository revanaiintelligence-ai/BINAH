"""
BINAH — WTM Integration Adapter

This module connects the WTM discovery layer with the BINAH
analytical layer.

Flow:

WTMOutput
    ↓
WTMAdapter
    ↓
AnalyzeRequest
    ↓
BINAH

WTM discovers and structures the case.
BINAH performs the business and need analysis.

This adapter does not perform BINAH methodology.
"""


from typing import Any

from app.models import AnalyzeRequest


class WTMIntegrationError(ValueError):
    """Raised when a WTM output cannot be sent to BINAH."""


class WTMAdapter:
    """
    Converts a validated WTM output into the BINAH API contract.
    """

    @staticmethod
    def validate_ready(wtm_output: Any) -> None:
        """
        Verify that WTM has explicitly marked the case as ready
        for BINAH.
        """

        if not getattr(wtm_output, "ready_for_binah", False):
            blocking_reasons = getattr(
                wtm_output,
                "blocking_reasons",
                [],
            )

            if blocking_reasons:
                reasons = "; ".join(
                    str(reason)
                    for reason in blocking_reasons
                )

                raise WTMIntegrationError(
                    f"WTM case is not ready for BINAH: {reasons}"
                )

            raise WTMIntegrationError(
                "WTM case is not ready for BINAH."
            )

    @staticmethod
    def to_binah_request(
        wtm_output: Any,
    ) -> AnalyzeRequest:
        """
        Convert a ready WTMOutput into BINAH AnalyzeRequest.
        """

        WTMAdapter.validate_ready(wtm_output)

        business = getattr(wtm_output, "business", None)
        context = getattr(wtm_output, "context", None)
        objective = getattr(wtm_output, "objective", None)
        evidence = getattr(wtm_output, "evidence", None)

        if not business:
            raise WTMIntegrationError(
                "WTM output does not contain a business."
            )

        if not context:
            raise WTMIntegrationError(
                "WTM output does not contain context."
            )

        if not objective:
            raise WTMIntegrationError(
                "WTM output does not contain objective."
            )

        evidence_payload = WTMAdapter._serialize_evidence(
            evidence
        )

        return AnalyzeRequest(
            business=business,
            context=context,
            objective=objective,
            evidence=evidence_payload,
        )

    @staticmethod
    def _serialize_evidence(
        evidence: Any,
    ) -> list[dict[str, Any]]:
        """
        Convert WTM evidence objects into plain dictionaries
        suitable for the BINAH API contract.
        """

        if not evidence:
            return []

        serialized = []

        for item in evidence:
            if hasattr(item, "model_dump"):
                serialized.append(
                    item.model_dump(mode="json")
                )
            elif isinstance(item, dict):
                serialized.append(item)
            else:
                serialized.append(
                    {
                        "content": str(item),
                    }
                )

        return serialized