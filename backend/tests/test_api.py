from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "ok"
    assert "mlops_layer" in data["layers"]


def test_predict():
    payload = {
        "inventory_level": 1500,
        "lead_time_days": 10,
        "historical_weekly_demand": 600,
        "supplier_reliability_score": 0.9,
    }
    r = client.post("/predict", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data["predicted_next_week_demand"] > 0


def test_qa_guardrail():
    out_scope = client.post("/qa", json={"question": "How do I bake a cake?"})
    assert out_scope.status_code == 200
    assert "only answer supply-chain" in out_scope.json()["answer"]

    in_scope = client.post("/qa", json={"question": "How does lead time affect forecast quality?"})
    assert in_scope.status_code == 200
    assert len(in_scope.json()["references"]) >= 1
