"""
BINAH — Opportunity Identification

Consolidates validated business, process, capability, solution,
AI, work, and agent findings into an actionable Opportunity Map.

This module identifies opportunities.
It does not execute solutions or AI systems.
"""

from typing import Any, Dict, List, Optional


OPPORTUNITY_TYPES = [
    "BUSINESS",
    "PROCESS",
    "TASK",
    "CAPABILITY",
    "SOFTWARE",
    "TRADITIONAL_AUTOMATION",
    "AI_NOW",
    "AI_LATER",
    "AI_PREPARATION",
    "ORGANIZATIONAL",
    "DATA",
    "KNOWLEDGE",
    "HYBRID",
]

OPPORTUNITY_STATUSES = [
    "IDENTIFIED",
    "PRIORITIZED",
    "RECOMMENDED",
    "DEFERRED",
    "NOT_RECOMMENDED",
]

AI_OPPORTUNITY_TYPES = [
    "AI_NOW",
    "AI_LATER",
    "AI_PREPARATION",
]

PRIORITY_LEVELS = [
    "LOW",
    "MEDIUM",
    "HIGH",
    "CRITICAL",
]


def identify_opportunities(
    *,
    need: Any,
    solution_evaluation: Optional[Dict[str, Any]] = None,
    ai_evaluation: Optional[Dict[str, Any]] = None,
    work_design: Optional[Dict[str, Any]] = None,
    agent_specification: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Identify and organize opportunities derived from BINAH analysis.

    Opportunities must remain traceable to the validated need and
    downstream analytical findings.
    """

    normalized_need = _normalize_need(need)

    if not normalized_need:
        return {
            "status": "NOT_IDENTIFIED",
            "need": None,
            "opportunities": [],
            "ai_opportunity_map": _empty_ai_opportunity_map(),
            "priority_order": [],
            "next_action": "Validate the business need before identifying opportunities.",
        }

    solutions = solution_evaluation or {}
    ai = ai_evaluation or {}
    work = work_design or {}
    agents = agent_specification or {}

    opportunities: List[Dict[str, Any]] = []

    opportunities.extend(
        _identify_solution_opportunities(
            need=normalized_need,
            solution_evaluation=solutions,
        )
    )

    opportunities.extend(
        _identify_work_opportunities(
            need=normalized_need,
            work_design=work,
        )
    )

    opportunities.extend(
        _identify_ai_opportunities(
            need=normalized_need,
            ai_evaluation=ai,
        )
    )

    opportunities.extend(
        _identify_agent_opportunities(
            need=normalized_need,
            agent_specification=agents,
        )
    )

    opportunities = _deduplicate_opportunities(opportunities)

    priority_order = _prioritize_opportunities(opportunities)

    ai_opportunity_map = build_ai_opportunity_map(
        ai_evaluation=ai,
        opportunities=opportunities,
    )

    return {
        "status": (
            "IDENTIFIED"
            if opportunities
            else "NO_OPPORTUNITIES_IDENTIFIED"
        ),
        "need": normalized_need,
        "opportunities": opportunities,
        "opportunity_count": len(opportunities),
        "priority_order": priority_order,
        "ai_opportunity_map": ai_opportunity_map,
        "validation": validate_opportunities(
            {
                "status": (
                    "IDENTIFIED"
                    if opportunities
                    else "NO_OPPORTUNITIES_IDENTIFIED"
                ),
                "need": normalized_need,
                "opportunities": opportunities,
            }
        ),
        "next_action": (
            "Prioritize and evaluate the identified opportunities."
            if opportunities
            else "Reassess the validated need and solution analysis."
        ),
    }


def create_opportunity(
    *,
    opportunity_type: str,
    title: str,
    description: str,
    source: str,
    priority: str = "MEDIUM",
    status: str = "IDENTIFIED",
    value: Any = None,
    friction: Any = None,
    prerequisites: Optional[List[str]] = None,
    risks: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Create a normalized opportunity record.
    """

    if opportunity_type not in OPPORTUNITY_TYPES:
        raise ValueError(
            f"Unsupported opportunity type: {opportunity_type}."
        )

    if priority not in PRIORITY_LEVELS:
        raise ValueError(
            f"Unsupported priority: {priority}."
        )

    if status not in OPPORTUNITY_STATUSES:
        raise ValueError(
            f"Unsupported opportunity status: {status}."
        )

    if not title.strip():
        raise ValueError("Opportunity title cannot be empty.")

    if not description.strip():
        raise ValueError(
            "Opportunity description cannot be empty."
        )

    return {
        "id": _make_opportunity_id(
            opportunity_type=opportunity_type,
            title=title,
        ),
        "type": opportunity_type,
        "title": title.strip(),
        "description": description.strip(),
        "source": source,
        "priority": priority,
        "status": status,
        "value": value,
        "friction": friction,
        "prerequisites": prerequisites or [],
        "risks": risks or [],
    }


def build_ai_opportunity_map(
    *,
    ai_evaluation: Optional[Dict[str, Any]] = None,
    opportunities: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    """
    Build the AI Opportunity Map.

    It explicitly distinguishes:
        AI now
        AI later
        AI preparation

    This prevents a "no AI now" conclusion from becoming a dead end.
    """

    ai = ai_evaluation or {}
    all_opportunities = opportunities or []

    current = ai.get("current_opportunities", [])
    future = ai.get("future_opportunities", [])
    readiness_gaps = ai.get("readiness_gaps", [])
    preparation_plan = ai.get("preparation_plan", [])
    evolution_path = ai.get("ai_evolution_path", [])

    ai_now = _normalize_items(current)
    ai_later = _normalize_items(future)
    ai_preparation = _normalize_items(readiness_gaps)

    opportunity_ai_now = [
        item
        for item in all_opportunities
        if item.get("type") == "AI_NOW"
    ]

    opportunity_ai_later = [
        item
        for item in all_opportunities
        if item.get("type") == "AI_LATER"
    ]

    opportunity_ai_preparation = [
        item
        for item in all_opportunities
        if item.get("type") == "AI_PREPARATION"
    ]

    return {
        "ai_outcome": ai.get("outcome"),
        "ai_now": ai_now,
        "ai_later": ai_later,
        "ai_preparation": ai_preparation,
        "current_opportunity_records": opportunity_ai_now,
        "future_opportunity_records": opportunity_ai_later,
        "preparation_opportunity_records": opportunity_ai_preparation,
        "readiness_gaps": ai_preparation,
        "preparation_plan": preparation_plan,
        "evolution_path": evolution_path,
        "human_role": ai.get("human_role"),
        "recommended_application_type": ai.get(
            "recommended_application_type"
        ),
    }


def prioritize_opportunities(
    opportunities: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """
    Assign priority to opportunities using available evidence.

    Priority is based on business relevance, value, friction,
    and whether the opportunity directly addresses the validated need.
    """

    prioritized = []

    for opportunity in opportunities:
        score = _priority_score(opportunity)

        item = dict(opportunity)
        item["priority_score"] = score
        item["status"] = "PRIORITIZED"
        item["priority"] = _score_to_priority(score)

        prioritized.append(item)

    prioritized.sort(
        key=lambda item: item.get("priority_score", 0),
        reverse=True,
    )

    return prioritized


def validate_opportunities(
    result: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Validate the structural integrity of an opportunity result.
    """

    if not isinstance(result, dict):
        return {
            "valid": False,
            "errors": ["Opportunity result must be a dictionary."],
        }

    errors: List[str] = []

    if not result.get("need"):
        errors.append(
            "A validated need is required."
        )

    opportunities = result.get("opportunities")

    if not isinstance(opportunities, list):
        errors.append(
            "opportunities must be a list."
        )
    else:
        for index, opportunity in enumerate(opportunities):
            if not isinstance(opportunity, dict):
                errors.append(
                    f"Opportunity at index {index} must be a dictionary."
                )
                continue

            if opportunity.get("type") not in OPPORTUNITY_TYPES:
                errors.append(
                    f"Invalid opportunity type at index {index}."
                )

            if not opportunity.get("title"):
                errors.append(
                    f"Opportunity at index {index} has no title."
                )

            if not opportunity.get("source"):
                errors.append(
                    f"Opportunity at index {index} has no source."
                )

    return {
        "valid": len(errors) == 0,
        "errors": errors,
    }


def get_opportunities(
    result: Dict[str, Any],
) -> List[Dict[str, Any]]:
    """
    Return identified opportunities from a result.
    """

    if not isinstance(result, dict):
        return []

    opportunities = result.get("opportunities")

    if isinstance(opportunities, list):
        return opportunities

    return []


def get_ai_opportunity_map(
    result: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Return the AI Opportunity Map from an opportunity result.
    """

    if not isinstance(result, dict):
        return _empty_ai_opportunity_map()

    ai_map = result.get("ai_opportunity_map")

    if isinstance(ai_map, dict):
        return ai_map

    return _empty_ai_opportunity_map()


def _identify_solution_opportunities(
    *,
    need: str,
    solution_evaluation: Dict[str, Any],
) -> List[Dict[str, Any]]:
    """
    Identify opportunities from solution evaluation.
    """

    opportunities: List[Dict[str, Any]] = []

    evaluated = solution_evaluation.get(
        "solutions",
        solution_evaluation.get("evaluated_solutions", []),
    )

    if not isinstance(evaluated, list):
        return opportunities

    for solution in evaluated:
        if not isinstance(solution, dict):
            continue

        status = solution.get("status")

        if status not in {
            "EVALUATED",
            "RECOMMENDED",
        }:
            continue

        result_type = solution.get("result_type")

        if not result_type:
            continue

        opportunity_type = _solution_to_opportunity_type(
            result_type
        )

        opportunities.append(
            create_opportunity(
                opportunity_type=opportunity_type,
                title=f"Opportunity: {result_type}",
                description=(
                    solution.get("recommendation")
                    or solution.get("description")
                    or f"Potential solution for: {need}"
                ),
                source="solution_evaluation",
                priority="MEDIUM",
                value=solution.get("value"),
                friction=solution.get("friction"),
                prerequisites=solution.get(
                    "prerequisites",
                    [],
                ),
                risks=solution.get(
                    "risks",
                    [],
                ),
            )
        )

    return opportunities


def _identify_work_opportunities(
    *,
    need: str,
    work_design: Dict[str, Any],
) -> List[Dict[str, Any]]:
    """
    Identify opportunities from work redesign.
    """

    opportunities: List[Dict[str, Any]] = []

    actions = work_design.get("actions", [])

    if not isinstance(actions, list):
        return opportunities

    for action in actions:
        if not isinstance(action, dict):
            continue

        action_type = action.get("action")

        if not action_type:
            continue

        opportunity_type = "PROCESS"

        if action_type in {
            "AUTOMATE",
        }:
            opportunity_type = "TRADITIONAL_AUTOMATION"

        if action_type in {
            "DIGITIZE",
        }:
            opportunity_type = "SOFTWARE"

        opportunities.append(
            create_opportunity(
                opportunity_type=opportunity_type,
                title=f"Work opportunity: {action_type}",
                description=(
                    action.get("description")
                    or f"Work redesign related to: {need}"
                ),
                source="work_design",
                priority="MEDIUM",
                value=action.get("value"),
                friction=action.get("friction"),
            )
        )

    return opportunities


def _identify_ai_opportunities(
    *,
    need: str,
    ai_evaluation: Dict[str, Any],
) -> List[Dict[str, Any]]:
    """
    Convert AI evaluation findings into explicit opportunities.
    """

    opportunities: List[Dict[str, Any]] = []

    current = ai_evaluation.get(
        "current_opportunities",
        [],
    )

    future = ai_evaluation.get(
        "future_opportunities",
        [],
    )

    preparation = ai_evaluation.get(
        "readiness_gaps",
        [],
    )

    for item in _normalize_items(current):
        opportunities.append(
            create_opportunity(
                opportunity_type="AI_NOW",
                title="AI opportunity now",
                description=item,
                source="ai_evaluation.current_opportunities",
                priority="HIGH",
            )
        )

    for item in _normalize_items(future):
        opportunities.append(
            create_opportunity(
                opportunity_type="AI_LATER",
                title="Future AI opportunity",
                description=item,
                source="ai_evaluation.future_opportunities",
                priority="MEDIUM",
            )
        )

    for item in _normalize_items(preparation):
        opportunities.append(
            create_opportunity(
                opportunity_type="AI_PREPARATION",
                title="AI readiness opportunity",
                description=item,
                source="ai_evaluation.readiness_gaps",
                priority="MEDIUM",
            )
        )

    return opportunities


def _identify_agent_opportunities(
    *,
    need: str,
    agent_specification: Dict[str, Any],
) -> List[Dict[str, Any]]:
    """
    Identify opportunities created by a justified agent architecture.
    """

    if agent_specification.get("status") != "SPECIFIED":
        return []

    agent_type = agent_specification.get(
        "agent_type",
        "SPECIALIZED_AGENT",
    )

    specification = agent_specification.get(
        "specification",
        {},
    )

    return [
        create_opportunity(
            opportunity_type="AI_NOW",
            title=f"Specialized agent opportunity: {agent_type}",
            description=(
                specification.get("purpose")
                or f"Specialized agent opportunity for: {need}"
            ),
            source="agent_specification",
            priority="HIGH",
            prerequisites=[
                "validated business need",
                "defined agent scope",
                "human governance",
                "required controls",
            ],
            risks=[
                "scope expansion",
                "incorrect outputs",
                "automation beyond authorization",
            ],
        )
    ]


def _solution_to_opportunity_type(
    result_type: str,
) -> str:
    """
    Map a solution result to an opportunity category.
    """

    mapping = {
        "NON_AI_SOLUTION_RECOMMENDED": "BUSINESS",
        "PROCESS_IMPROVEMENT_RECOMMENDED": "PROCESS",
        "SOFTWARE_RECOMMENDED": "SOFTWARE",
        "TRADITIONAL_AUTOMATION_RECOMMENDED": (
            "TRADITIONAL_AUTOMATION"
        ),
        "AI_OPTIONAL": "AI_LATER",
        "AI_USEFUL": "AI_NOW",
        "AI_RECOMMENDED": "AI_NOW",
        "AI_NOT_JUSTIFIED": "AI_PREPARATION",
        "AI_INAPPROPRIATE": "PROCESS",
        "HYBRID_SOLUTION_RECOMMENDED": "HYBRID",
    }

    return mapping.get(
        result_type,
        "BUSINESS",
    )


def _prioritize_opportunities(
    opportunities: List[Dict[str, Any]],
) -> List[str]:
    """
    Return opportunity IDs in priority order.
    """

    prioritized = prioritize_opportunities(
        opportunities
    )

    return [
        item["id"]
        for item in prioritized
        if item.get("id")
    ]


def _priority_score(
    opportunity: Dict[str, Any],
) -> int:
    """
    Calculate a deterministic priority score.
    """

    score = 0

    priority = opportunity.get("priority")

    score += {
        "LOW": 1,
        "MEDIUM": 2,
        "HIGH": 3,
        "CRITICAL": 4,
    }.get(priority, 0)

    opportunity_type = opportunity.get("type")

    if opportunity_type in {
        "AI_NOW",
        "PROCESS",
        "CAPABILITY",
    }:
        score += 1

    if opportunity.get("value") not in (
        None,
        "",
        [],
        {},
    ):
        score += 1

    if opportunity.get("friction") not in (
        None,
        "",
        [],
        {},
    ):
        score += 1

    return score


def _score_to_priority(
    score: int,
) -> str:
    """
    Convert a numeric priority score to a priority level.
    """

    if score >= 7:
        return "CRITICAL"

    if score >= 5:
        return "HIGH"

    if score >= 3:
        return "MEDIUM"

    return "LOW"


def _normalize_items(
    value: Any,
) -> List[str]:
    """
    Normalize strings or structured items into descriptions.
    """

    if value is None:
        return []

    if isinstance(value, str):
        return [value.strip()] if value.strip() else []

    if not isinstance(value, list):
        return []

    result: List[str] = []

    for item in value:
        if isinstance(item, str):
            text = item.strip()

            if text:
                result.append(text)

        elif isinstance(item, dict):
            for key in (
                "description",
                "opportunity",
                "title",
                "gap",
                "need",
            ):
                candidate = item.get(key)

                if isinstance(candidate, str) and candidate.strip():
                    result.append(candidate.strip())
                    break

    return _unique(result)


def _deduplicate_opportunities(
    opportunities: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """
    Remove duplicate opportunity records.
    """

    result: List[Dict[str, Any]] = []
    seen = set()

    for opportunity in opportunities:
        key = (
            opportunity.get("type"),
            opportunity.get("title"),
            opportunity.get("description"),
        )

        if key in seen:
            continue

        seen.add(key)
        result.append(opportunity)

    return result


def _make_opportunity_id(
    *,
    opportunity_type: str,
    title: str,
) -> str:
    """
    Generate a deterministic, readable opportunity identifier.
    """

    normalized = (
        title.lower()
        .replace(" ", "_")
        .replace("-", "_")
        .replace("/", "_")
    )

    normalized = "".join(
        character
        for character in normalized
        if character.isalnum() or character == "_"
    )

    return f"OPP_{opportunity_type}_{normalized[:60]}"


def _normalize_need(
    need: Any,
) -> str:
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


def _unique(
    values: List[str],
) -> List[str]:
    """
    Preserve order while removing duplicate strings.
    """

    result: List[str] = []
    seen = set()

    for value in values:
        normalized = value.strip()

        if normalized and normalized not in seen:
            result.append(normalized)
            seen.add(normalized)

    return result


def _empty_ai_opportunity_map() -> Dict[str, Any]:
    """
    Return an empty but structurally valid AI Opportunity Map.
    """

    return {
        "ai_outcome": None,
        "ai_now": [],
        "ai_later": [],
        "ai_preparation": [],
        "current_opportunity_records": [],
        "future_opportunity_records": [],
        "preparation_opportunity_records": [],
        "readiness_gaps": [],
        "preparation_plan": [],
        "evolution_path": [],
        "human_role": None,
        "recommended_application_type": None,
    }