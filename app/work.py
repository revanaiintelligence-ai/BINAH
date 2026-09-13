from typing import Any, Dict, List, Optional


WORK_RESULT_TYPES = [
    "WORK_STRUCTURE_RECOMMENDED",
    "PROCESS_IMPROVEMENT_RECOMMENDED",
    "SOFTWARE_RECOMMENDED",
    "TRADITIONAL_AUTOMATION_RECOMMENDED",
    "HYBRID_WORK_STRUCTURE",
    "NO_WORK_CHANGE_REQUIRED",
]


WORK_ACTION_TYPES = [
    "KEEP",
    "ELIMINATE",
    "COMBINE",
    "DELEGATE",
    "STANDARDIZE",
    "AUTOMATE",
    "DIGITIZE",
    "CONTROL",
    "REASSIGN",
    "MEASURE",
    "REDESIGN",
]


def design_work(
    *,
    need: Any,
    second_decomposition: Any,
    ai_evaluation: Any = None,
) -> Dict[str, Any]:
    """
    Design the required work structure after the need and task
    decomposition have been validated.

    This stage determines how work should be organized independently
    of whether AI is eventually used.
    """

    normalized_need = _normalize_need(need)
    tasks = _extract_tasks(second_decomposition)

    if not normalized_need:
        return {
            "status": "STOP_NEED_NOT_VALIDATED",
            "need": normalized_need,
            "work_structure": [],
            "actions": [],
            "result": "NO_WORK_CHANGE_REQUIRED",
            "next_action": (
                "Validate the business need before designing work."
            ),
        }

    if not tasks:
        return {
            "status": "NO_TASKS_AVAILABLE",
            "need": normalized_need,
            "work_structure": [],
            "actions": [],
            "result": "NO_WORK_CHANGE_REQUIRED",
            "next_action": (
                "Complete second-level task decomposition "
                "before designing the work structure."
            ),
        }

    work_structure = []

    for task in tasks:
        if not isinstance(task, dict):
            continue

        work_structure.append(
            {
                "area": task.get("area"),
                "function": task.get("function"),
                "process": task.get("process"),
                "activity": task.get("activity"),
                "task": task.get("task"),
                "responsible": task.get("actor"),
                "tools": task.get("tools", []),
                "flow": task.get("flow"),
                "current_state": task.get("current_state"),
                "target_state": task.get("target_state"),
            }
        )

    return {
        "status": "WORK_DESIGN_READY",
        "need": normalized_need,
        "work_structure": work_structure,
        "actions": [],
        "result": None,
        "ai_relationship": _summarize_ai_relationship(
            ai_evaluation
        ),
        "next_action": (
            "Evaluate whether tasks should be retained, "
            "eliminated, combined, delegated, standardized, "
            "automated, digitized, controlled, reassigned, "
            "measured or redesigned."
        ),
    }


def define_work_action(
    work_design: Dict[str, Any],
    *,
    task: str,
    action: str,
    rationale: str,
    responsible: Any = None,
    tool: Any = None,
    expected_effect: Any = None,
    priority: str = "MEDIUM",
) -> Dict[str, Any]:
    """
    Define an explicit work-design action.
    """

    if action not in WORK_ACTION_TYPES:
        raise ValueError(
            f"Invalid work action: {action}"
        )

    if priority not in {
        "LOW",
        "MEDIUM",
        "HIGH",
        "CRITICAL",
    }:
        raise ValueError(
            "priority must be LOW, MEDIUM, HIGH or CRITICAL."
        )

    normalized_task = str(task).strip()
    normalized_rationale = str(rationale).strip()

    if not normalized_task:
        raise ValueError("task cannot be empty.")

    if not normalized_rationale:
        raise ValueError(
            "A rationale is required for a work action."
        )

    work_action = {
        "task": normalized_task,
        "action": action,
        "rationale": normalized_rationale,
        "responsible": responsible,
        "tool": tool,
        "expected_effect": expected_effect,
        "priority": priority,
    }

    work_design.setdefault(
        "actions",
        [],
    ).append(work_action)

    work_design["status"] = "WORK_ACTIONS_DEFINED"

    return work_design


def define_work_structure(
    work_design: Dict[str, Any],
    *,
    area: str,
    function: str,
    process: str,
    activity: str,
    task: str,
    responsible: str,
    tools: Optional[List[str]] = None,
    flow: Optional[str] = None,
    current_state: Any = None,
    target_state: Any = None,
) -> Dict[str, Any]:
    """
    Add a structured work element.
    """

    structure_item = {
        "area": str(area).strip(),
        "function": str(function).strip(),
        "process": str(process).strip(),
        "activity": str(activity).strip(),
        "task": str(task).strip(),
        "responsible": str(responsible).strip(),
        "tools": list(tools or []),
        "flow": flow,
        "current_state": current_state,
        "target_state": target_state,
    }

    required_fields = [
        "area",
        "function",
        "process",
        "activity",
        "task",
        "responsible",
    ]

    for field in required_fields:
        if not structure_item[field]:
            raise ValueError(
                f"{field} cannot be empty."
            )

    work_design.setdefault(
        "work_structure",
        []
    ).append(structure_item)

    work_design["status"] = "WORK_STRUCTURE_DEFINED"

    return work_design


def assign_work_tool(
    work_design: Dict[str, Any],
    *,
    task: str,
    tool: str,
    rationale: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Assign a tool to a task without assuming that the tool must be AI.
    """

    normalized_task = str(task).strip()
    normalized_tool = str(tool).strip()

    if not normalized_task:
        raise ValueError("task cannot be empty.")

    if not normalized_tool:
        raise ValueError("tool cannot be empty.")

    for item in work_design.setdefault(
        "work_structure",
        [],
    ):
        if item.get("task") == normalized_task:
            item.setdefault("tools", []).append(
                normalized_tool
            )

            if rationale is not None:
                item["tool_rationale"] = (
                    str(rationale).strip()
                )

            return work_design

    raise ValueError(
        f"Task not found in work structure: {normalized_task}"
    )


def apply_work_action(
    work_design: Dict[str, Any],
    *,
    task: str,
    action: str,
    target_responsible: Any = None,
    target_tool: Any = None,
    target_process: Any = None,
) -> Dict[str, Any]:
    """
    Apply a structural action to an existing work element.

    This records the intended target state; it does not execute
    operational changes in an external system.
    """

    if action not in WORK_ACTION_TYPES:
        raise ValueError(
            f"Invalid work action: {action}"
        )

    normalized_task = str(task).strip()

    for item in work_design.setdefault(
        "work_structure",
        [],
    ):
        if item.get("task") != normalized_task:
            continue

        item["proposed_action"] = action

        if target_responsible is not None:
            item["target_responsible"] = target_responsible

        if target_tool is not None:
            item["target_tool"] = target_tool

        if target_process is not None:
            item["target_process"] = target_process

        return work_design

    raise ValueError(
        f"Task not found in work structure: {normalized_task}"
    )


def finalize_work_design(
    work_design: Dict[str, Any],
    *,
    result: str,
    rationale: str,
) -> Dict[str, Any]:
    """
    Finalize the recommended work structure.
    """

    if result not in WORK_RESULT_TYPES:
        raise ValueError(
            f"Invalid work result: {result}"
        )

    normalized_rationale = str(rationale).strip()

    if not normalized_rationale:
        raise ValueError(
            "A rationale is required to finalize work design."
        )

    work_design["result"] = result
    work_design["rationale"] = normalized_rationale
    work_design["status"] = "WORK_DESIGN_FINALIZED"

    return work_design


def validate_work_design(
    work_design: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Validate the work-design structure.
    """

    errors: List[str] = []

    if not isinstance(work_design, dict):
        return {
            "valid": False,
            "errors": [
                "work_design must be a dictionary."
            ],
        }

    if not work_design.get("need"):
        errors.append("Missing need.")

    if not isinstance(
        work_design.get("work_structure", []),
        list,
    ):
        errors.append(
            "work_structure must be a list."
        )

    if not isinstance(
        work_design.get("actions", []),
        list,
    ):
        errors.append(
            "actions must be a list."
        )

    for index, item in enumerate(
        work_design.get("work_structure", [])
    ):
        if not isinstance(item, dict):
            errors.append(
                f"Work structure item {index} must be a dictionary."
            )
            continue

        for field in [
            "area",
            "function",
            "process",
            "activity",
            "task",
            "responsible",
        ]:
            if not item.get(field):
                errors.append(
                    f"Work structure item {index} "
                    f"is missing {field}."
                )

    for index, action in enumerate(
        work_design.get("actions", [])
    ):
        if not isinstance(action, dict):
            errors.append(
                f"Work action {index} must be a dictionary."
            )
            continue

        if not action.get("task"):
            errors.append(
                f"Work action {index} is missing task."
            )

        action_type = action.get("action")

        if action_type not in WORK_ACTION_TYPES:
            errors.append(
                f"Invalid work action at index {index}: "
                f"{action_type}"
            )

    return {
        "valid": len(errors) == 0,
        "errors": errors,
    }


def get_work_actions(
    work_design: Dict[str, Any],
) -> List[Dict[str, Any]]:
    """
    Return the defined work-design actions.
    """

    return list(
        work_design.get(
            "actions",
            [],
        )
    )


def get_work_structure(
    work_design: Dict[str, Any],
) -> List[Dict[str, Any]]:
    """
    Return the current/proposed work structure.
    """

    return list(
        work_design.get(
            "work_structure",
            [],
        )
    )


def _extract_tasks(
    second_decomposition: Any,
) -> List[Any]:
    """
    Normalize second-level task decomposition output.
    """

    if isinstance(second_decomposition, dict):
        tasks = second_decomposition.get(
            "tasks",
            []
        )

        if isinstance(tasks, list):
            return tasks

        decomposition = second_decomposition.get(
            "decomposition"
        )

        if isinstance(decomposition, list):
            return decomposition

        return []

    if isinstance(second_decomposition, list):
        return second_decomposition

    return []


def _normalize_need(
    need: Any,
) -> str:
    """
    Normalize a BINAH need into a readable statement.
    """

    if isinstance(need, str):
        return need.strip()

    if isinstance(need, dict):
        statement = need.get("statement")

        if statement:
            return str(statement).strip()

        return str(need).strip()

    if need is None:
        return ""

    return str(need).strip()


def _summarize_ai_relationship(
    ai_evaluation: Any,
) -> Dict[str, Any]:
    """
    Describe how work design relates to the AI evaluation.

    Work design remains valid even when AI is recommended.
    """

    if not isinstance(ai_evaluation, dict):
        return {
            "available": False,
            "outcome": None,
            "role": "INDEPENDENT_WORK_DESIGN",
        }

    return {
        "available": True,
        "outcome": ai_evaluation.get("outcome"),
        "role": (
            "WORK_STRUCTURE_REMAINS_REQUIRED"
        ),
    }