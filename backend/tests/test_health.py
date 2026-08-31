import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_openapi_docs():
    response = client.get("/api/openapi.json")
    assert response.status_code == 200
    assert "paths" in response.json()
    assert "/api/health" in response.json()["paths"]
