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
            "problem": "Sales leads are not being followed up consistently.",
            "business_context": "Small real estate business.",
            "current_process": "Leads are handled manually through WhatsApp.",
            "desired_outcome": "Improve follow-up consistency.",
            "constraints": ["Limited staff"],
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["problem"] == "Sales leads are not being followed up consistently."
    assert "need" in data
    assert "gap" in data
    assert "alternatives" in data
    assert "ai_relevance" in data
    assert "next_action" in data