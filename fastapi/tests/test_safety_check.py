# tests/test_safety_check.py

from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_safety_check():
    response = client.post("/safety-check", json={"query": "Should I take tamoxifen?"})
    assert response.status_code == 200
    data = response.json()
    assert "is_medical_diagnosis" in data
