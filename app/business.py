from typing import Any, Dict, List


BUSINESS_LEVELS = [
    "business",
    "area",
    "function",
    "process",
    "activity",
    "task",
]


def decompose_business(
    *,
    business: str,
    context: str = "",
) -> Dict[str, Any]:
    """
    Perform BINAH's initial business decomposition.

    Structure:
    Business
        → Areas
            → Functions
                → Processes
                    → Activities
                        → Tasks

    This module establishes the operational structure of the business
    before identifying and diagnosing a specific need.
    """

    business_name = business.strip()
    business_context = context.strip()

    if not business_name:
        raise ValueError("Business is required.")

    business_map = {
        "business": business_name,
        "context": business_context,
        "areas": [],
    }

    return {
        "status": "READY_FOR_NEED_DISCOVERY",
        "levels": BUSINESS_LEVELS,
        "business_map": business_map,
        "structure": {
            "business": business_name,
            "areas": [],
        },
        "decomposition": {
            "area": [],
            "function": [],
            "process": [],
            "activity": [],
            "task": [],
        },
    }


def add_area(
    business_map: Dict[str, Any],
    *,
    name: str,
    description: str = "",
) -> Dict[str, Any]:
    """
    Add an operational area to the Business Operational Map.
    """

    area_name = name.strip()

    if not area_name:
        raise ValueError("Area name is required.")

    area = {
        "name": area_name,
        "description": description.strip(),
        "functions": [],
    }

    business_map.setdefault("areas", []).append(area)

    return business_map


def add_function(
    business_map: Dict[str, Any],
    *,
    area: str,
    name: str,
    description: str = "",
) -> Dict[str, Any]:
    """
    Add a function to an existing business area.
    """

    area_name = area.strip()
    function_name = name.strip()

    if not area_name:
        raise ValueError("Area is required.")

    if not function_name:
        raise ValueError("Function name is required.")

    target_area = _find_area(business_map, area_name)

    target_area["functions"].append(
        {
            "name": function_name,
            "description": description.strip(),
            "processes": [],
        }
    )

    return business_map


def add_process(
    business_map: Dict[str, Any],
    *,
    area: str,
    function: str,
    name: str,
    description: str = "",
) -> Dict[str, Any]:
    """
    Add a process to an existing business function.
    """

    target_function = _find_function(
        business_map,
        area.strip(),
        function.strip(),
    )

    process_name = name.strip()

    if not process_name:
        raise ValueError("Process name is required.")

    target_function["processes"].append(
        {
            "name": process_name,
            "description": description.strip(),
            "activities": [],
        }
    )

    return business_map


def add_activity(
    business_map: Dict[str, Any],
    *,
    area: str,
    function: str,
    process: str,
    name: str,
    description: str = "",
) -> Dict[str, Any]:
    """
    Add an activity to an existing business process.
    """

    target_process = _find_process(
        business_map,
        area.strip(),
        function.strip(),
        process.strip(),
    )

    activity_name = name.strip()

    if not activity_name:
        raise ValueError("Activity name is required.")

    target_process["activities"].append(
        {
            "name": activity_name,
            "description": description.strip(),
            "tasks": [],
        }
    )

    return business_map


def add_task(
    business_map: Dict[str, Any],
    *,
    area: str,
    function: str,
    process: str,
    activity: str,
    name: str,
    description: str = "",
    actor: str = "",
) -> Dict[str, Any]:
    """
    Add a task to an existing business activity.
    """

    target_activity = _find_activity(
        business_map,
        area.strip(),
        function.strip(),
        process.strip(),
        activity.strip(),
    )

    task_name = name.strip()

    if not task_name:
        raise ValueError("Task name is required.")

    target_activity["tasks"].append(
        {
            "name": task_name,
            "description": description.strip(),
            "actor": actor.strip(),
        }
    )

    return business_map


def validate_business_map(
    business_map: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Validate the basic structural integrity of a Business Operational Map.
    """

    errors: List[str] = []

    if not business_map.get("business"):
        errors.append("Business is missing.")

    if "areas" not in business_map:
        errors.append("Areas structure is missing.")

    return {
        "valid": not errors,
        "errors": errors,
        "status": (
            "VALID"
            if not errors
            else "INVALID"
        ),
    }


def _find_area(
    business_map: Dict[str, Any],
    area_name: str,
) -> Dict[str, Any]:

    for area in business_map.get("areas", []):
        if area["name"].lower() == area_name.lower():
            return area

    raise ValueError(
        f"Area not found: {area_name}"
    )


def _find_function(
    business_map: Dict[str, Any],
    area_name: str,
    function_name: str,
) -> Dict[str, Any]:

    target_area = _find_area(
        business_map,
        area_name,
    )

    for function in target_area.get("functions", []):
        if function["name"].lower() == function_name.lower():
            return function

    raise ValueError(
        f"Function not found: {function_name}"
    )


def _find_process(
    business_map: Dict[str, Any],
    area_name: str,
    function_name: str,
    process_name: str,
) -> Dict[str, Any]:

    target_function = _find_function(
        business_map,
        area_name,
        function_name,
    )

    for process in target_function.get("processes", []):
        if process["name"].lower() == process_name.lower():
            return process

    raise ValueError(
        f"Process not found: {process_name}"
    )


def _find_activity(
    business_map: Dict[str, Any],
    area_name: str,
    function_name: str,
    process_name: str,
    activity_name: str,
) -> Dict[str, Any]:

    target_process = _find_process(
        business_map,
        area_name,
        function_name,
        process_name,
    )

    for activity in target_process.get("activities", []):
        if activity["name"].lower() == activity_name.lower():
            return activity

    raise ValueError(
        f"Activity not found: {activity_name}"
    )