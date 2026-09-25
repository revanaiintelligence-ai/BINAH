from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


BUSINESS = "Empresa de servicios profesionales"

CONTEXT = (
    "La empresa recibe solicitudes de clientes por distintos canales "
    "y actualmente el seguimiento se realiza manualmente."
)

OBJECTIVE = (
    "Reducir el tiempo de respuesta y mejorar la capacidad de seguimiento "
    "sin comprometer la responsabilidad humana."
)


NEED = {
    "statement": (
        "La empresa necesita reducir el tiempo de respuesta "
        "y mejorar el seguimiento de solicitudes."
    ),
    "type": "speed",
    "area": "Atención al cliente",
    "function": "Gestión de solicitudes",
    "process": "Recepción y seguimiento",
    "activity": "Clasificación y seguimiento",
    "task": "Clasificar solicitudes recibidas",
    "actor": "Personal de atención",
}


EVIDENCE = [
    {
        "source": "Registro operativo",
        "observation": (
            "Las solicitudes permanecen sin seguimiento durante varias horas."
        ),
    }
]


REALITY_GATE_VALIDATED = {
    "need": NEED,
    "evidence": EVIDENCE,
    "consequences": (
        "Las demoras generan pérdida de oportunidades y "
        "aumentan la carga operativa."
    ),
    "exists": True,
    "wants_to_solve": True,
    "capability_insufficient": True,
}


BUSINESS_MAP = {
    "business": BUSINESS,
    "context": CONTEXT,
    "areas": [],
}


SECOND_DECOMPOSITION = {
    "status": "SECOND_DECOMPOSITION_READY",
    "decomposition_allowed": True,
    "need": NEED,
    "business_map": BUSINESS_MAP,
    "location": {
        "area": NEED["area"],
        "function": NEED["function"],
        "process": NEED["process"],
        "activity": NEED["activity"],
        "task": NEED["task"],
        "actor": NEED["actor"],
    },
    "levels": [
        "need",
        "area",
        "function",
        "process",
        "activity",
        "task",
        "actor",
    ],
    "variables": [],
    "tasks": [],
}


ALTERNATIVES = {
    "status": "READY_FOR_ALTERNATIVE_EVALUATION",
    "need": NEED,
    "second_decomposition": SECOND_DECOMPOSITION,
    "alternatives": [
        {
            "type": "HUMAN",
            "status": "PENDING_EVALUATION",
        },
        {
            "type": "PROCESS",
            "status": "PENDING_EVALUATION",
        },
        {
            "type": "SOFTWARE",
            "status": "PENDING_EVALUATION",
        },
        {
            "type": "TRADITIONAL_AUTOMATION",
            "status": "PENDING_EVALUATION",
        },
        {
            "type": "AI",
            "status": "PENDING_EVALUATION",
        },
        {
            "type": "HYBRID",
            "status": "PENDING_EVALUATION",
        },
    ],
}


def test_root():
    response = client.get("/")

    assert response.status_code == 200
    data = response.json()

    assert data["name"] == "BINAH API"
    assert data["methodology"] == "BINAH"
    assert data["version"] == "0.2"
    assert data["status"] == "operational"


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    data = response.json()

    assert data["status"] == "ok"
    assert data["version"] == "0.2"


def test_complete_binah_analysis():
    response = client.post(
        "/v1/binah/analyze",
        json={
            "business": BUSINESS,
            "context": CONTEXT,
            "objective": OBJECTIVE,
            "evidence": EVIDENCE,
        },
    )

    assert response.status_code == 200
    data = response.json()

    assert data["methodology"] == "BINAH"
    assert data["version"] == "0.2"
    assert data["business"] is not None
    assert data["business_map"] is not None
    assert data["need"] is not None
    assert data["capability"] is not None
    assert data["reality_gate"] is not None

    assert data["second_decomposition"] is not None
    assert data["alternatives"] is not None
    assert data["solution_evaluation"] is not None
    assert data["ai_evaluation"] is not None
    assert data["work_design"] is not None
    assert data["agent_specification"] is not None
    assert data["opportunities"] is not None
    assert data["diagnostic"] is not None


def test_business_decomposition():
    response = client.post(
        "/v1/business/decompose",
        json={
            "business": BUSINESS,
            "context": CONTEXT,
        },
    )

    assert response.status_code == 200
    data = response.json()

    assert data["status"] == "READY_FOR_NEED_DISCOVERY"
    assert data["business_map"]["business"] == BUSINESS
    assert data["business_map"]["context"] == CONTEXT
    assert data["business_map"]["areas"] == []


def test_need_identification_contract():
    response = client.post(
        "/v1/needs/identify",
        json={
            "business": BUSINESS,
            "objective": OBJECTIVE,
            "context": CONTEXT,
            "evidence": EVIDENCE,
        },
    )

    assert response.status_code == 200
    data = response.json()

    assert data["status"] == "NEED_HYPOTHESIS"
    assert data["business"] == BUSINESS
    assert data["objective"] == OBJECTIVE
    assert "need" in data
    assert "validation" in data
    assert data["validation"]["identified"] is True
    assert data["validation"]["validated"] is False


def test_capability_diagnosis():
    response = client.post(
        "/v1/capability/diagnose",
        json={
            "need": NEED,
            "business_map": BUSINESS_MAP,
        },
    )

    assert response.status_code == 200
    data = response.json()

    assert "status" in data
    assert "required_capability" in data
    assert "current_capability" in data
    assert "gap" in data


def test_reality_gate_validated():
    response = client.post(
        "/v1/gates/reality",
        json=REALITY_GATE_VALIDATED,
    )

    assert response.status_code == 200
    data = response.json()

    assert data["status"] == "VALIDATED"
    assert data["validated"] is True
    assert all(data["criteria"].values())


def test_reality_gate_rejects_invalid_need():
    response = client.post(
        "/v1/gates/reality",
        json={
            "need": NEED,
            "evidence": [],
            "consequences": None,
            "exists": False,
            "wants_to_solve": False,
            "capability_insufficient": False,
        },
    )

    assert response.status_code == 200
    data = response.json()

    assert data["status"] == "REJECTED"
    assert data["validated"] is False
    assert data["failed_criteria"]


def test_task_decomposition_requires_reality_gate():
    response = client.post(
        "/v1/tasks/decompose",
        json={
            "need": NEED,
            "business_map": BUSINESS_MAP,
            "reality_gate": {
                "status": "STOP_NEED_NOT_VALIDATED",
                "validated": False,
            },
        },
    )

    assert response.status_code == 200
    data = response.json()

    assert data["status"] == "STOP_NEED_NOT_VALIDATED"
    assert data["decomposition_allowed"] is False
    assert data["tasks"] == []


def test_task_decomposition_after_reality_gate():
    response = client.post(
        "/v1/tasks/decompose",
        json={
            "need": NEED,
            "business_map": BUSINESS_MAP,
            "reality_gate": {
                "status": "VALIDATED",
                "validated": True,
            },
        },
    )

    assert response.status_code == 200
    data = response.json()

    assert data["status"] == "SECOND_DECOMPOSITION_READY"
    assert data["decomposition_allowed"] is True
    assert data["tasks"] == []


def test_alternatives_evaluation():
    response = client.post(
        "/v1/alternatives/evaluate",
        json={
            "need": NEED,
            "second_decomposition": SECOND_DECOMPOSITION,
        },
    )

    assert response.status_code == 200
    data = response.json()

    assert data["status"] == "READY_FOR_ALTERNATIVE_EVALUATION"
    assert len(data["alternatives"]) == 6

    alternative_types = {
        alternative["type"]
        for alternative in data["alternatives"]
    }

    assert alternative_types == {
        "HUMAN",
        "PROCESS",
        "SOFTWARE",
        "TRADITIONAL_AUTOMATION",
        "AI",
        "HYBRID",
    }


def test_solution_evaluation_pending_before_alternative_evaluation():
    response = client.post(
        "/v1/solutions/evaluate",
        json={
            "need": NEED,
            "alternatives": ALTERNATIVES,
        },
    )

    assert response.status_code == 200
    data = response.json()

    assert data["status"] == "READY_FOR_SOLUTION_EVALUATION"
    assert data["evaluated_count"] == 0
    assert data["selected_solution"] is None
    assert data["result"] is None


def test_ai_evaluation_pending_without_evaluated_ai_solution():
    response = client.post(
        "/v1/ai/evaluate",
        json={
            "need": NEED,
            "task": SECOND_DECOMPOSITION,
            "alternatives": ALTERNATIVES,
            "solution_evaluation": {
                "need": NEED,
                "solutions": [
                    {
                        "type": "AI",
                        "status": "PENDING_EVALUATION",
                    }
                ],
                "evaluated_count": 0,
            },
        },
    )

    assert response.status_code == 200
    data = response.json()

    assert data["status"] == "AI_EVALUATION_PENDING"
    assert data["outcome"] is None
    assert data["decision_ready"] is False


def test_work_design():
    response = client.post(
        "/v1/work/design",
        json={
            "need": NEED,
            "second_decomposition": SECOND_DECOMPOSITION,
            "ai_evaluation": {
                "status": "AI_EVALUATION_PENDING",
                "outcome": None,
                "decision_ready": False,
            },
        },
    )

    assert response.status_code == 200
    data = response.json()

    assert "status" in data
    assert "work_structure" in data
    assert "tasks" in data


def test_agent_specification_not_justified_without_agent_decision():
    response = client.post(
        "/v1/agents/specify",
        json={
            "need": NEED,
            "ai_evaluation": {
                "status": "AI_EVALUATION_PENDING",
                "outcome": None,
                "decision_ready": False,
            },
            "work_design": {
                "status": "WORK_STRUCTURE_RECOMMENDED",
                "work_structure": [],
            },
            "solution_evaluation": {
                "need": NEED,
                "solutions": [],
                "evaluated_count": 0,
            },
        },
    )

    assert response.status_code == 200
    data = response.json()

    assert data["status"] == "NOT_JUSTIFIED"


def test_opportunity_identification():
    response = client.post(
        "/v1/opportunities/identify",
        json={
            "need": NEED,
            "solution_evaluation": {
                "need": NEED,
                "solutions": [],
                "evaluated_count": 0,
                "selected_solution": None,
                "result": None,
            },
            "ai_evaluation": {
                "status": "AI_EVALUATION_PENDING",
                "outcome": None,
                "decision_ready": False,
                "current_opportunities": [],
                "future_opportunities": [],
                "readiness_gaps": [],
            },
            "work_design": {
                "status": "WORK_STRUCTURE_RECOMMENDED",
                "work_structure": [],
            },
            "agent_specification": {
                "status": "NOT_JUSTIFIED",
            },
        },
    )

    assert response.status_code == 200
    data = response.json()

    assert "status" in data
    assert "opportunities" in data
    assert "ai_opportunity_map" in data


def test_diagnostic_generation():
    response = client.post(
        "/v1/diagnostic/generate",
        json={
            "business": BUSINESS,
            "context": CONTEXT,
            "objective": OBJECTIVE,
            "need": NEED,
            "capability": {
                "status": "CAPABILITY_DIAGNOSIS_READY",
                "required_capability": None,
                "current_capability": None,
                "gap": None,
            },
            "gap": None,
            "reality_gate": {
                "status": "VALIDATED",
                "validated": True,
            },
            "alternatives": ALTERNATIVES,
            "solution_evaluation": {
                "need": NEED,
                "solutions": [],
                "evaluated_count": 0,
                "selected_solution": None,
                "result": None,
            },
            "ai_evaluation": {
                "status": "AI_EVALUATION_PENDING",
                "outcome": None,
                "decision_ready": False,
                "current_opportunities": [],
                "future_opportunities": [],
                "readiness_gaps": [],
            },
            "work_design": {
                "status": "WORK_STRUCTURE_RECOMMENDED",
                "work_structure": [],
            },
            "agent_specification": {
                "status": "NOT_JUSTIFIED",
            },
            "opportunities": {
                "status": "OPPORTUNITIES_IDENTIFIED",
                "opportunities": [],
                "ai_opportunity_map": {},
            },
        },
    )

    assert response.status_code == 200
    data = response.json()

    assert "status" in data
    assert "result" in data
    assert "business" in data
    assert "need" in data
    assert "reality_gate" in data

Este archivo sustituye completo al actual "tests/test_api.py". Después de subirlo, ejecuta CI. El resultado que buscamos es 29/29, y si aparece otro fallo no modificamos más tests a ciegas: revisamos exactamente qué contrato está fallando.