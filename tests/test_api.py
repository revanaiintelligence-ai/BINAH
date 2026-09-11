from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["status"] == "operational"


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_analyze():
    response = client.post(
        "/analyze",
        json={
            "problem": "Customer requests are not being followed up consistently.",
            "business_context": "Small service business.",
            "current_process": "Requests are handled manually through multiple channels.",
            "desired_outcome": "Improve follow-up consistency.",
            "constraints": ["Limited staff"],
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["problem"] == "Customer requests are not being followed up consistently."
    assert "need" in data
    assert "gap" in data
    assert "alternatives" in data
    assert "ai_relevance" in data
    assert "next_action" in data


def test_capability_diagnose():
    response = client.post(
        "/capability/diagnose",
        params={
            "need": "Follow up with every qualified customer request.",
            "current_capability": "Manual follow-up across multiple channels.",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["need"] == "Follow up with every qualified customer request."
    assert data["current_capability"] == "Manual follow-up across multiple channels."
    assert "gap" in data
    assert "next_action" in data


def test_reality_gate_validated():
    response = client.post(
        "/reality-gate",
        json={
            "need": "Follow up with every qualified customer request.",
            "evidence": [
                {
                    "source": "Business records",
                    "observation": "Qualified requests are frequently not followed up.",
                    "date": "2026-09-11",
                    "reliability": "high",
                }
            ],
            "relevant_consequences": "Lost customer opportunities.",
            "exists_currently": True,
            "desired_by_business": True,
            "capability_insufficient": True,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["validated"] is True
    assert data["status"] == "NEED_VALIDATED"
    assert data["failed_conditions"] == []


def test_reality_gate_stop():
    response = client.post(
        "/reality-gate",
        json={
            "need": "Automate a process that has not been demonstrated as necessary.",
            "evidence": [],
            "relevant_consequences": "No relevant consequences established.",
            "exists_currently": False,
            "desired_by_business": False,
            "capability_insufficient": False,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["validated"] is False
    assert data["status"] == "STOP_NEED_NOT_VALIDATED"
    assert data["decision"] == "STOP — Need Not Validated"
    assert len(data["failed_conditions"]) > 0