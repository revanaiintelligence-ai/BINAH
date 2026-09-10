from app.models import AnalyzeRequest, AnalyzeResponse


def analyze(request: AnalyzeRequest) -> AnalyzeResponse:
    problem = request.problem.strip()

    context = request.business_context or "No business context provided."
    process = request.current_process or "No current process provided."
    outcome = request.desired_outcome or "No desired outcome provided."

    diagnosis = (
        f"The reported problem is: {problem}. "
        f"Context: {context}. "
        f"Current process: {process}."
    )

    need = (
        f"Clarify the underlying business need required to achieve: {outcome}."
    )

    gap = (
        "The capability gap cannot yet be fully determined. "
        "Further analysis of the current capability and alternatives is required."
    )

    alternatives = [
        "Improve the existing process.",
        "Use an existing non-AI solution.",
        "Introduce AI only if it provides a measurable advantage.",
    ]

    ai_relevance = (
        "Undetermined. AI should be evaluated only after the need, "
        "capability gap, and existing alternatives are understood."
    )

    next_action = (
        "Collect evidence about the current process, existing capabilities, "
        "constraints, and available alternatives before selecting a solution."
    )

    return AnalyzeResponse(
        problem=problem,
        diagnosis=diagnosis,
        need=need,
        gap=gap,
        alternatives=alternatives,
        ai_relevance=ai_relevance,
        next_action=next_action,
    )