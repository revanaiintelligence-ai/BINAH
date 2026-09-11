from typing import Optional


def decompose_task(
    need: str,
    area: str,
    function: str,
    process: str,
    activity: str,
    task: str,
    actor: str,
    frequency: Optional[str] = None,
    time_required: Optional[str] = None,
    volume: Optional[str] = None,
    input_data: Optional[str] = None,
    decision: Optional[str] = None,
    complexity: Optional[str] = None,
    errors: Optional[str] = None,
    dependency: Optional[str] = None,
    repetition: Optional[str] = None,
    bottleneck: Optional[str] = None,
) -> dict:
    return {
        "need": need.strip(),
        "area": area.strip(),
        "function": function.strip(),
        "process": process.strip(),
        "activity": activity.strip(),
        "task": task.strip(),
        "actor": actor.strip(),
        "variables": {
            "frequency": frequency,
            "time_required": time_required,
            "volume": volume,
            "input": input_data,
            "decision": decision,
            "complexity": complexity,
            "errors": errors,
            "dependency": dependency,
            "repetition": repetition,
            "bottleneck": bottleneck,
        },
    }