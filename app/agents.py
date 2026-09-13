"""
BINAH — Specialized Agent Architecture

Defines specialized AI-agent specifications only when the BINAH
analysis establishes that an agent is justified.

This module does not execute agents.
It specifies what an agent would need to do, why it is justified,
what inputs it requires, what outputs it produces, and where the
human remains responsible.
"""

from typing import Any, Dict, List, Optional


AGENT_STATUSES = [
    "NOT_JUSTIFIED",
    "JUSTIFIED",
    "SPECIFIED",
]

AGENT_TYPES = [
    "SPECIALIZED_AGENT",
    "MULTI_AGENT",
]

AGENT_ROLES = [
    "H0",
    "H1",
    "H2",
    "H3",
]

AGENT_COMPONENTS = [
    "purpose",
    "scope",
    "inputs",
    "knowledge",
    "reasoning",
    "actions",
    "outputs",
    "controls",
    "human_role",
    "escalation",
    "monitoring",
]

AGENT_JUSTIFICATION_RESULTS = [
    "AGENT_NOT_JUSTIFIED",
    "AGENT_JUSTIFIED",
    "MULTI_AGENT_JUSTIFIED",
]


def specify_agent(
    *,
    need: Any,
    ai_evaluation: Optional[Dict[str, Any]] = None,
    work_design: Optional[Dict[str, Any]] = None,
    solution_evaluation: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Produce a specialized-agent specification when justified.

    Agent architecture is downstream of:
        Need → Capability → Reality Gate → Decomposition
        → Alternatives → Solution → AI Evaluation → Work Design

    The function does not build or execute an agent.
    """

    normalized_need = _normalize_need(need)

    if not normalized_need:
        return _stop_result(
            reason="No validated need was provided.",
        )

    ai = ai_evaluation or {}
    work = work_design or {}
    solutions = solution_evaluation or {}

    ai_outcome = ai.get("outcome")
    recommended_application = ai.get("recommended_application_type")

    if not _agent_is_justified(
        ai_evaluation=ai,
        solution_evaluation=solutions,
    ):
        return {
            "status": "NOT_JUSTIFIED",
            "justification_result": "AGENT_NOT_JUSTIFIED",
            "need": normalized_need,
            "agent_type": None,
            "specification": None,
            "human_role": ai.get("human_role"),
            "reason": (
                "The available analysis does not establish sufficient "
                "business justification for a specialized AI agent."
            ),
            "next_action": (
                "Use the recommended non-agent solution or continue "
                "with work/process design."
            ),
        }

    agent_type = _determine_agent_type(ai)

    specification = {
        "purpose": normalized_need,
        "scope": _define_scope(
            need=normalized_need,
            ai_evaluation=ai,
            work_design=work,
        ),
        "inputs": _define_inputs(
            ai_evaluation=ai,
            work_design=work,
        ),
        "knowledge": _define_knowledge_requirements(
            ai_evaluation=ai,
        ),
        "reasoning": _define_reasoning_requirements(
            ai_evaluation=ai,
        ),
        "actions": _define_actions(
            ai_evaluation=ai,
            work_design=work,
        ),
        "outputs": _define_outputs(
            ai_evaluation=ai,
        ),
        "controls": _define_controls(
            ai_evaluation=ai,
        ),
        "human_role": define_agent_human_role(
            ai_evaluation=ai,
        ),
        "escalation": _define_escalation(
            ai_evaluation=ai,
        ),
        "monitoring": _define_monitoring(
            ai_evaluation=ai,
        ),
    }

    return {
        "status": "SPECIFIED",
        "justification_result": (
            "MULTI_AGENT_JUSTIFIED"
            if agent_type == "MULTI_AGENT"
            else "AGENT_JUSTIFIED"
        ),
        "need": normalized_need,
        "agent_type": agent_type,
        "recommended_application_type": recommended_application,
        "ai_outcome": ai_outcome,
        "specification": specification,
        "human_role": specification["human_role"],
        "work_relationship": _summarize_work_relationship(work),
        "validation": validate_agent_specification(
            {
                "status": "SPECIFIED",
                "agent_type": agent_type,
                "specification": specification,
            }
        ),
    }


def define_agent_scope(
    *,
    purpose: str,
    scope: Optional[List[str]] = None,
    exclusions: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Define the operational boundary of a specialized agent.
    """

    if not isinstance(purpose, str) or not purpose.strip():
        raise ValueError("purpose must be a non-empty string.")

    return {
        "purpose": purpose.strip(),
        "included": scope or [],
        "excluded": exclusions or [],
    }


def define_agent_human_role(
    *,
    ai_evaluation: Optional[Dict[str, Any]] = None,
    role: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Explicitly define the human role in an agent-supported workflow.

    H0 = human retains full responsibility.
    H1 = human supervises AI assistance.
    H2 = human validates important AI outputs/actions.
    H3 = AI may execute bounded actions while human retains governance.
    """

    ai = ai_evaluation or {}

    selected_role = role or ai.get("human_role") or "H2"

    if selected_role not in AGENT_ROLES:
        raise ValueError(
            f"Unsupported human role: {selected_role}. "
            f"Expected one of {AGENT_ROLES}."
        )

    descriptions = {
        "H0": (
            "Human performs the work and retains full responsibility; "
            "the AI agent is not authorized to perform operational actions."
        ),
        "H1": (
            "Human supervises the AI agent and remains responsible for "
            "the resulting work."
        ),
        "H2": (
            "Human validates important outputs or decisions before "
            "operational use."
        ),
        "H3": (
            "AI may perform bounded operational actions under predefined "
            "controls, escalation rules, and human governance."
        ),
    }

    return {
        "level": selected_role,
        "description": descriptions[selected_role],
        "responsibility": "HUMAN",
        "autonomy": selected_role == "H3",
        "requires_governance": True,
    }


def define_agent_controls(
    *,
    controls: Optional[List[str]] = None,
    risk_level: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Define governance and operational controls for the agent.
    """

    selected_controls = controls or [
        "input_validation",
        "output_validation",
        "permission_boundaries",
        "human_escalation",
        "activity_logging",
        "error_handling",
    ]

    return {
        "risk_level": risk_level or "UNASSESSED",
        "controls": selected_controls,
        "human_override": True,
        "auditability": True,
    }


def validate_agent_specification(
    specification: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Validate the structural completeness of an agent specification.
    """

    if not isinstance(specification, dict):
        return {
            "valid": False,
            "errors": ["Specification must be a dictionary."],
        }

    errors: List[str] = []

    status = specification.get("status")
    agent_type = specification.get("agent_type")
    details = specification.get("specification")

    if status not in AGENT_STATUSES:
        errors.append("Invalid agent status.")

    if status == "SPECIFIED":
        if agent_type not in AGENT_TYPES:
            errors.append("Invalid agent type.")

        if not isinstance(details, dict):
            errors.append("Agent specification must be a dictionary.")
        else:
            for component in AGENT_COMPONENTS:
                if component not in details:
                    errors.append(
                        f"Missing required agent component: {component}."
                    )

            human_role = details.get("human_role")
            if not isinstance(human_role, dict):
                errors.append("Human role must be explicitly defined.")
            elif human_role.get("level") not in AGENT_ROLES:
                errors.append("Invalid human-role level.")

    return {
        "valid": len(errors) == 0,
        "errors": errors,
    }


def get_agent_specification(
    result: Dict[str, Any],
) -> Optional[Dict[str, Any]]:
    """
    Return the specification from a successful agent analysis.
    """

    if not isinstance(result, dict):
        return None

    specification = result.get("specification")

    if isinstance(specification, dict):
        return specification

    return None


def _agent_is_justified(
    *,
    ai_evaluation: Dict[str, Any],
    solution_evaluation: Dict[str, Any],
) -> bool:
    """
    Determine whether an AI agent is sufficiently justified.

    A generic AI recommendation is not automatically an agent
    recommendation. The analysis must specifically support agentic
    execution or a comparable autonomous workflow.
    """

    outcome = ai_evaluation.get("outcome")
    application = ai_evaluation.get("recommended_application_type")

    if outcome not in {"AI_NOW", "AI_PREPARATION"}:
        return False

    if application in {"AI_AGENT", "AI_MULTI_AGENT"}:
        return True

    recommended = solution_evaluation.get("recommended_solution")

    if isinstance(recommended, dict):
        result_type = recommended.get("result_type")

        if result_type == "AI_RECOMMENDED":
            recommendation_text = str(
                recommended.get("recommendation", "")
            ).lower()

            if "agent" in recommendation_text:
                return True

    return False


def _determine_agent_type(
    ai_evaluation: Dict[str, Any],
) -> str:
    """
    Determine whether the justified architecture is single-agent
    or multi-agent.
    """

    application = ai_evaluation.get(
        "recommended_application_type"
    )

    if application == "AI_MULTI_AGENT":
        return "MULTI_AGENT"

    return "SPECIALIZED_AGENT"


def _define_scope(
    *,
    need: str,
    ai_evaluation: Dict[str, Any],
    work_design: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Define what the agent is and is not responsible for.
    """

    opportunities = ai_evaluation.get(
        "current_opportunities",
        [],
    )

    return {
        "purpose": need,
        "tasks": opportunities,
        "limitations": [
            "must operate within the validated business need",
            "must not expand scope without authorization",
            "must not replace undefined human accountability",
        ],
    }


def _define_inputs(
    *,
    ai_evaluation: Dict[str, Any],
    work_design: Dict[str, Any],
) -> List[str]:
    """
    Identify expected inputs from the analyzed workflow.
    """

    inputs: List[str] = []

    for key in (
        "inputs",
        "required_inputs",
        "data_requirements",
    ):
        value = ai_evaluation.get(key)

        if isinstance(value, list):
            inputs.extend(str(item) for item in value)

    tasks = work_design.get("tasks")

    if isinstance(tasks, list):
        for task in tasks:
            if isinstance(task, dict):
                input_value = task.get("input")

                if input_value:
                    inputs.append(str(input_value))

    if not inputs:
        inputs = [
            "validated business information",
            "relevant task inputs",
            "authorized contextual information",
        ]

    return _unique(inputs)


def _define_knowledge_requirements(
    *,
    ai_evaluation: Dict[str, Any],
) -> List[str]:
    """
    Identify knowledge sources the agent would require.
    """

    knowledge = ai_evaluation.get("knowledge")

    if isinstance(knowledge, list):
        return _unique([str(item) for item in knowledge])

    return [
        "business rules",
        "validated process information",
        "authorized reference information",
    ]


def _define_reasoning_requirements(
    *,
    ai_evaluation: Dict[str, Any],
) -> List[str]:
    """
    Define the reasoning responsibilities without implementing them.
    """

    reasoning = ai_evaluation.get("reasoning")

    if isinstance(reasoning, list):
        return _unique([str(item) for item in reasoning])

    return [
        "interpret relevant inputs",
        "apply validated business rules",
        "identify uncertainty",
        "produce traceable conclusions",
        "escalate decisions outside authorized scope",
    ]


def _define_actions(
    *,
    ai_evaluation: Dict[str, Any],
    work_design: Dict[str, Any],
) -> List[str]:
    """
    Define permitted actions without granting unrestricted autonomy.
    """

    actions = ai_evaluation.get("actions")

    if isinstance(actions, list):
        return _unique([str(item) for item in actions])

    work_actions = work_design.get("actions")

    if isinstance(work_actions, list):
        extracted = []

        for action in work_actions:
            if isinstance(action, dict):
                value = action.get("action")

                if value:
                    extracted.append(str(value))

        if extracted:
            return _unique(extracted)

    return [
        "analyze",
        "classify",
        "prepare",
        "recommend",
        "escalate",
    ]


def _define_outputs(
    *,
    ai_evaluation: Dict[str, Any],
) -> List[str]:
    """
    Define expected outputs of the agent.
    """

    outputs = ai_evaluation.get("outputs")

    if isinstance(outputs, list):
        return _unique([str(item) for item in outputs])

    return [
        "traceable analysis",
        "finding",
        "recommendation",
        "uncertainty or escalation signal",
    ]


def _define_controls(
    *,
    ai_evaluation: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Define controls using AI risk information when available.
    """

    risks = ai_evaluation.get("risks")

    controls = [
        "input_validation",
        "scope_control",
        "output_validation",
        "human_escalation",
        "activity_logging",
        "permission_boundaries",
    ]

    if isinstance(risks, list) and risks:
        controls.append("risk_specific_controls")

    return define_agent_controls(
        controls=controls,
        risk_level=(
            ai_evaluation.get("risk_level")
            or "UNASSESSED"
        ),
    )


def _define_escalation(
    *,
    ai_evaluation: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Define conditions under which the agent must stop or escalate.
    """

    return {
        "required": True,
        "conditions": [
            "insufficient information",
            "low confidence",
            "outside authorized scope",
            "material business consequence",
            "conflicting information",
            "policy or rule exception",
        ],
        "destination": "HUMAN",
    }


def _define_monitoring(
    *,
    ai_evaluation: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Define monitoring requirements.
    """

    return {
        "required": True,
        "metrics": [
            "task_completion",
            "error_rate",
            "escalation_rate",
            "human_override_rate",
            "output_quality",
            "business_impact",
        ],
        "review": "HUMAN_GOVERNED",
    }


def _summarize_work_relationship(
    work_design: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Explain how the proposed agent relates to the work design.
    """

    if not isinstance(work_design, dict):
        return {
            "work_design_available": False,
            "relationship": "UNDEFINED",
        }

    return {
        "work_design_available": True,
        "relationship": (
            "Agent supports or performs only the work activities "
            "explicitly justified by the BINAH analysis."
        ),
    }


def _normalize_need(need: Any) -> str:
    """
    Normalize need information from string or structured output.
    """

    if isinstance(need, str):
        return need.strip()

    if isinstance(need, dict):
        for key in (
            "statement",
            "need",
            "description",
            "name",
        ):
            value = need.get(key)

            if isinstance(value, str) and value.strip():
                return value.strip()

    return ""


def _stop_result(
    *,
    reason: str,
) -> Dict[str, Any]:
    """
    Standard stop result.
    """

    return {
        "status": "NOT_JUSTIFIED",
        "justification_result": "AGENT_NOT_JUSTIFIED",
        "need": None,
        "agent_type": None,
        "specification": None,
        "human_role": {
            "level": "H0",
            "responsibility": "HUMAN",
        },
        "reason": reason,
        "next_action": "Return to need validation and solution evaluation.",
    }


def _unique(values: List[str]) -> List[str]:
    """
    Preserve order while removing duplicate values.
    """

    result: List[str] = []
    seen = set()

    for value in values:
        normalized = value.strip()

        if normalized and normalized not in seen:
            result.append(normalized)
            seen.add(normalized)

    return result