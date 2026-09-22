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
            "tasks": tasks,
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
            "tasks": [],
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
        "tasks": tasks,
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


def _normalize_need(
    need: Any,
) -> Any:
    """
    Normalize the need without changing its semantic content.
    """

    if need is None:
        return None

    if isinstance(need, dict):
        if not need:
            return None

        if need.get("status") in {
            "NEED_NOT_IDENTIFIED",
            "NEED_HYPOTHESIS",
            "STOP_NEED_NOT_VALIDATED",
        }:
            if not need.get("need"):
                return None

        return need.get("need", need)

    if isinstance(need, str):
        value = need.strip()
        return value if value else None

    return need


def _extract_tasks(
    second_decomposition: Any,
) -> List[Dict[str, Any]]:
    """
    Extract task-level elements from the second decomposition.

    The function accepts the existing BINAH decomposition structures
    without imposing a new schema.
    """

    if not second_decomposition:
        return []

    if isinstance(second_decomposition, list):
        return [
            item
            for item in second_decomposition
            if isinstance(item, dict)
        ]

    if not isinstance(second_decomposition, dict):
        return []

    tasks = second_decomposition.get("tasks")

    if isinstance(tasks, list):
        return [
            item
            for item in tasks
            if isinstance(item, dict)
        ]

    decomposition = second_decomposition.get(
        "decomposition"
    )

    if isinstance(decomposition, list):
        return [
            item
            for item in decomposition
            if isinstance(item, dict)
        ]

    return []


def _summarize_ai_relationship(
    ai_evaluation: Any,
) -> Dict[str, Any]:
    """
    Summarize the relationship between work design and AI.

    Work design remains independent from the decision to use AI.
    """

    if not ai_evaluation:
        return {
            "evaluated": False,
            "relevance": None,
        }

    if isinstance(ai_evaluation, dict):
        return {
            "evaluated": True,
            "relevance": ai_evaluation.get(
                "relevance",
                ai_evaluation.get("status"),
            ),
        }

    return {
        "evaluated": True,
        "relevance": str(ai_evaluation),
    }


def define_work_action(
    *,
    task: Any,
    action: str,
    rationale: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Define an action to apply to a task.
    """

    if action not in WORK_ACTION_TYPES:
        raise ValueError(
            f"Invalid work action: {action}"
        )

    return {
        "task": task,
        "action": action,
        "rationale": rationale,
    }


def define_work_structure(
    *,
    tasks: List[Dict[str, Any]],
    actions: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    """
    Build a structured work-design object.
    """

    return {
        "tasks": tasks,
        "actions": actions or [],
    }