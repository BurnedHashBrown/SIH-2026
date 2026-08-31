import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.config import settings

client = TestClient(app)


@pytest.fixture
def auth_headers():
    response = client.post(
        "/api/auth/login",
        json={
            "email": settings.SEED_INSPECTOR_EMAIL,
            "password": settings.SEED_INSPECTOR_PASSWORD,
        },
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_generate_pdf_report_and_download(auth_headers):
    # 1. Generate PDF Report
    report_resp = client.post(
        "/api/inspections/LM-2026-0248/report",
        headers=auth_headers,
    )
    assert report_resp.status_code == 201
    report_data = report_resp.json()
    assert report_data["report_number"].startswith("REP-")
    report_id = report_data["id"]

    # 2. Get Report Metadata
    meta_resp = client.get(f"/api/reports/{report_id}", headers=auth_headers)
    assert meta_resp.status_code == 200
    assert meta_resp.json()["id"] == report_id

    # 3. Download PDF Report
    dl_resp = client.get(f"/api/reports/{report_id}/download", headers=auth_headers)
    assert dl_resp.status_code == 200
    assert dl_resp.headers["content-type"] == "application/pdf"
    assert dl_resp.content.startswith(b"%PDF")


def test_dashboard_summary_and_violations(auth_headers):
    # Summary
    summary_resp = client.get("/api/dashboard/summary", headers=auth_headers)
    assert summary_resp.status_code == 200
    s_data = summary_resp.json()
    assert "total_inspections" in s_data
    assert "compliant" in s_data
    assert "requires_review" in s_data
    assert s_data["total_inspections"] >= 1

    # Violations breakdown
    viol_resp = client.get("/api/dashboard/violations", headers=auth_headers)
    assert viol_resp.status_code == 200
    v_data = viol_resp.json()
    assert "consumer_care" in v_data
    assert "mrp" in v_data
    assert "net_quantity" in v_data

    # Recent inspections
    recent_resp = client.get("/api/dashboard/recent-inspections", headers=auth_headers)
    assert recent_resp.status_code == 200
    items = recent_resp.json()
    assert isinstance(items, list)
    assert len(items) >= 1


def test_rules_api(auth_headers):
    rules_resp = client.get("/api/rules", headers=auth_headers)
    assert rules_resp.status_code == 200
    rules = rules_resp.json()
    assert len(rules) >= 6
    assert any(r["rule_code"] == "LM-001" for r in rules)
    assert any(r["rule_code"] == "LM-006" for r in rules)
