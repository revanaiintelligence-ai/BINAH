from typing import Any, Dict, List, Optional


TASK_VARIABLES = [
    "actor",
    "frequency",
    "time",
    "volume",
    "input",
    "information",
    "documents",
    "decision",
    "complexity",
    "errors",
    "dependency",
    "human_role",
    "repetition",
    "bottleneck",
    "efficiency",
    "improvement",
]


def decompose_need_tasks(
    *,
    need: Dict[str, Any],
    business_map: Dict[str, Any],
    reality_gate: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Perform the second-level decomposition of the area affected
    by a validated business need.

    BINAH sequence:

    Need
        ↓
    Area
        ↓
    Function
        ↓
    Process
        ↓
    Activity
        ↓
    Task
        ↓
    Actor

    This module is executed only after the Reality Gate.

    It does not select a solution and does not determine whether
    AI should be used.
    """

    gate_validated = bool(
        reality_gate.get("validated", False)
    )

    if not gate_validated:
        return {
            "status": "STOP_NEED_NOT_VALIDATED",
            "decomposition_allowed": False,
            "reason": (
                "Second-level task decomposition cannot proceed "
                "because the need has not passed the Reality Gate."
            ),
            "need": need,
            "business_map": business_map,
            "tasks": [],
        }

    normalized_need = _normalize_need(need)

    location = {
        "area": normalized_need.get("area"),
        "function": normalized_need.get("function"),
        "process": normalized_need.get("process"),
        "activity": normalized_need.get("activity"),
        "task": normalized_need.get("task"),
        "actor": normalized_need.get("actor"),
    }

    return {
        "status": "SECOND_DECOMPOSITION_READY",
        "decomposition_allowed": True,
        "need": normalized_need,
        "business_map": business_map,
        "location": location,
        "levels": [
            "need",
            "area",
            "function",
            "process",
            "activity",
            "task",
            "actor",
        ],
        "variables": TASK_VARIABLES,
        "tasks": [],
        "next_action": (
            "Populate the affected task and evaluate its operational "
            "characteristics before comparing alternatives."
        ),
    }


def define_task(
    decomposition: Dict[str, Any],
    *,
    area: str,
    function: str,
    process: str,
    activity: str,
    task: str,
    actor: str,
    frequency: Optional[str] = None,
    time: Optional[str] = None,
    volume: Optional[str] = None,
    input_data: Optional[str] = None,
    information: Optional[str] = None,
    documents: Optional[str] = None,
    decision: Optional[str] = None,
    complexity: Optional[str] = None,
    errors: Optional[str] = None,
    dependency: Optional[str] = None,
    human_role: Optional[str] = None,
    repetition: Optional[str] = None,
    bottleneck: Optional[str] = None,
    efficiency: Optional[str] = None,
    improvement: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Add a fully defined operational task to the second-level
    decomposition.
    """

    if not decomposition.get("decomposition_allowed", False):
        raise ValueError(
            "Task decomposition is not allowed before the Reality Gate."
        )

    normalized_task = {
        "area": _required_text(area, "Area"),
        "function": _required_text(function, "Function"),
        "process": _required_text(process, "Process"),
        "activity": _required_text(activity, "Activity"),
        "task": _required_text(task, "Task"),
        "actor": _required_text(actor, "Actor"),
        "variables": {
            "frequency": frequency,
            "time": time,
            "volume": volume,
            "input": input_data,
            "information": information,
            "documents": documents,
            "decision": decision,
            "complexity": complexity,
            "errors": errors,
            "dependency": dependency,
            "human_role": human_role,
            "repetition": repetition,
            "bottleneck": bottleneck,
            "efficiency": efficiency,
            "improvement": improvement,
        },
    }

    updated = dict(decomposition)

    existing_tasks = list(
        decomposition.get("tasks", [])
    )

    existing_tasks.append(normalized_task)

    updated["tasks"] = existing_tasks
    updated["status"] = "TASKS_DECOMPOSED"

    return updated


def add_task(
    decomposition: Dict[str, Any],
    task: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Add an already normalized task record.
    """

    if not decomposition.get("decomposition_allowed", False):
        raise ValueError(
            "Task decomposition is not allowed before the Reality Gate."
        )

    if not isinstance(task, dict):
        raise ValueError(
            "Task must be a dictionary."
        )

    required_fields = [
        "area",
        "function",
        "process",
        "activity",
        "task",
        "actor",
    ]

    missing_fields = [
        field
        for field in required_fields
        if not _value_exists(task.get(field))
    ]

    if missing_fields:
        raise ValueError(
            "Task is missing required fields: "
            + ", ".join(missing_fields)
        )

    updated = dict(decomposition)

    existing_tasks = list(
        decomposition.get("tasks", [])
    )

    existing_tasks.append(dict(task))

    updated["tasks"] = existing_tasks
    updated["status"] = "TASKS_DECOMPOSED"

    return updated


def validate_task_decomposition(
    decomposition: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Validate the structural completeness of a second-level
    task decomposition.
    """

    errors: List[str] = []

    if not decomposition.get(
        "decomposition_allowed",
        False,
    ):
        errors.append(
            "Task decomposition was not authorized by the Reality Gate."
        )

    if not decomposition.get("need"):
        errors.append(
            "Need is missing."
        )

    tasks = decomposition.get("tasks")

    if not isinstance(tasks, list):
        errors.append(
            "Tasks must be a list."
        )
    else:
        for index, task in enumerate(tasks):
            if not isinstance(task, dict):
                errors.append(
                    f"Task at index {index} is not a dictionary."
                )
                continue

            for field in [
                "area",
                "function",
                "process",
                "activity",
                "task",
                "actor",
            ]:
                if not _value_exists(task.get(field)):
                    errors.append(
                        f"Task at index {index} is missing '{field}'."
                    )

    return {
        "valid": not errors,
        "status": "VALID" if not errors else "INVALID",
        "errors": errors,
    }


def get_tasks(
    decomposition: Dict[str, Any],
) -> List[Dict[str, Any]]:
    """
    Return the task records from a decomposition.
    """

    tasks = decomposition.get("tasks", [])

    if not isinstance(tasks, list):
        return []

    return list(tasks)


def identify_task_characteristics(
    task: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Extract the operational characteristics of a task.

    This function describes the task. It does not recommend
    technology or AI.
    """

    if not isinstance(task, dict):
        raise ValueError(
            "Task must be a dictionary."
        )

    characteristics = {
        "actor": task.get("actor"),
        "frequency": _get_variable(task, "frequency"),
        "time": _get_variable(task, "time"),
        "volume": _get_variable(task, "volume"),
        "input": _get_variable(task, "input"),
        "information": _get_variable(task, "information"),
        "documents": _get_variable(task, "documents"),
        "decision": _get_variable(task, "decision"),
        "complexity": _get_variable(task, "complexity"),
        "errors": _get_variable(task, "errors"),
        "dependency": _get_variable(task, "dependency"),
        "human_role": _get_variable(task, "human_role"),
        "repetition": _get_variable(task, "repetition"),
        "bottleneck": _get_variable(task, "bottleneck"),
        "efficiency": _get_variable(task, "efficiency"),
        "improvement": _get_variable(task, "improvement"),
    }

    return {
        "task": task.get("task"),
        "characteristics": characteristics,
    }


def _normalize_need(
    need: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Normalize the need structure without changing its meaning.
    """

    if not isinstance(need, dict):
        raise ValueError(
            "Need must be a dictionary."
        )

    nested_need = need.get("need")

    if isinstance(nested_need, dict):
        return dict(nested_need)

    return dict(need)


def _required_text(
    value: Any,
    field_name: str,
) -> str:
    """
    Validate and normalize required textual fields.
    """

    if not isinstance(value, str):
        raise ValueError(
            f"{field_name} must be a string."
        )

    normalized = value.strip()

    if not normalized:
        raise ValueError(
            f"{field_name} is required."
        )

    return normalized


def _value_exists(
    value: Any,
) -> bool:
    """
    Determine whether a value contains usable information.
    """

    if value is None:
        return False

    if isinstance(value, str):
        return bool(value.strip())

    if isinstance(value, (list, tuple, set, dict)):
        return len(value) > 0

    return True


def _get_variable(
    task: Dict[str, Any],
    variable: str,
) -> Any:
    """
    Read a task variable from the normalized variables container.
    """

    variables = task.get("variables")

    if not isinstance(variables, dict):
        return None

    return variables.get(variable)