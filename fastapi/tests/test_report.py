# tests/test_report.py

from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_report_submission():
    response = client.post("/report", json={
        "user_id": "test_user",
        "query": "What diet helps after chemotherapy?",
        "classification": "medium",
        "feedback": "helpful"
    })
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
