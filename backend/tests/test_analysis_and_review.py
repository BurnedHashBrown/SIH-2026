import io
import pytest
from PIL import Image
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


def create_image_bytes():
    img = Image.new("RGB", (800, 1000), color=(240, 240, 240))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return buf.getvalue()


def test_full_analysis_workflow(auth_headers):
    # 1. Create inspection
    insp_resp = client.post(
        "/api/inspections",
        json={
            "product_name": "ABC Premium Biscuits",
            "brand": "ABC Foods",
            "category": "Food",
            "manufacturer": "ABC Foods Pvt. Ltd.",
            "batch_number": "B240826",
            "location": "Mumbai",
        },
        headers=auth_headers,
    )
    assert insp_resp.status_code == 201
    insp_id = insp_resp.json()["inspection_id"]

    # 2. Upload packaging image
    files = {"file": ("front_panel.jpg", create_image_bytes(), "image/jpeg")}
    upload_resp = client.post(
        f"/api/inspections/{insp_id}/images",
        files=files,
        data={"panel_type": "FRONT"},
        headers=auth_headers,
    )
    assert upload_resp.status_code == 201

    # 3. Trigger full AI analysis
    analyze_resp = client.post(
        f"/api/inspections/{insp_id}/analyze",
        headers=auth_headers,
    )
    assert analyze_resp.status_code == 200
    analysis = analyze_resp.json()

    assert analysis["inspection_id"] == insp_id
    assert analysis["compliance_score"] >= 80.0
    assert "summary" in analysis
    assert "declarations" in analysis
    assert len(analysis["declarations"]) >= 6

    # Verify extracted MRP and Net Quantity
    mrp_decl = next((d for d in analysis["declarations"] if d["type"] == "MRP"), None)
    assert mrp_decl is not None
    assert mrp_decl["status"] == "DETECTED"


def test_inspector_review_and_evidence(auth_headers):
    # Retrieve seeded inspection with violation
    detail_resp = client.get("/api/inspections/LM-2026-0248", headers=auth_headers)
    assert detail_resp.status_code == 200
    violations = detail_resp.json()["violations"]
    assert len(violations) > 0
    violation_id = violations[0]["id"]

    # 1. Check evidence endpoint
    ev_resp = client.get(f"/api/violations/{violation_id}/evidence", headers=auth_headers)
    assert ev_resp.status_code == 200
    assert ev_resp.json()["violation_id"] == violation_id

    # 2. Submit inspector review (CONFIRM finding)
    review_payload = {
        "decision": "CONFIRM",
        "remarks": "Consumer care information not visible on submitted packaging panels.",
    }
    rev_resp = client.post(
        f"/api/violations/{violation_id}/review",
        json=review_payload,
        headers=auth_headers,
    )
    assert rev_resp.status_code == 201
    rev_data = rev_resp.json()
    assert rev_data["decision"] == "CONFIRM"
    assert "Consumer care" in rev_data["remarks"]
