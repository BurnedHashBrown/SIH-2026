import io
import pytest
from PIL import Image
from fastapi.testclient import TestClient
from app.main import app
from app.config import settings
from app.ai.preprocessing import image_preprocessor

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


def create_sample_image_bytes(width=600, height=800, color=(255, 255, 255)) -> bytes:
    """Helper to create test image bytes."""
    img = Image.new("RGB", (width, height), color=color)
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return buf.getvalue()


def test_upload_valid_image(auth_headers):
    img_bytes = create_sample_image_bytes(800, 1000)
    files = {"file": ("packaging_front.jpg", img_bytes, "image/jpeg")}
    data = {"panel_type": "FRONT"}

    response = client.post(
        "/api/inspections/LM-2026-0248/images",
        files=files,
        data=data,
        headers=auth_headers,
    )
    assert response.status_code == 201
    resp_json = response.json()
    assert resp_json["panel_type"] == "FRONT"
    assert resp_json["quality_score"] > 0
    assert resp_json["width"] == 800
    assert resp_json["height"] == 1000
    assert "image_id" in resp_json


def test_upload_invalid_file_extension(auth_headers):
    files = {"file": ("script.txt", b"Hello text file", "text/plain")}
    response = client.post(
        "/api/inspections/LM-2026-0248/images",
        files=files,
        headers=auth_headers,
    )
    assert response.status_code == 400
    assert response.json()["error"]["code"] == "INVALID_FILE_TYPE"


def test_image_quality_preprocessor():
    # Test quality assessment on sharp white image
    img_bytes = create_sample_image_bytes(800, 800)
    result = image_preprocessor.assess_quality(image_bytes=img_bytes)
    assert result.quality_score >= 0.0
    assert isinstance(result.warnings, list)
    assert isinstance(result.is_acceptable, bool)


def test_list_inspection_images(auth_headers):
    response = client.get("/api/inspections/LM-2026-0248/images", headers=auth_headers)
    assert response.status_code == 200
    images = response.json()
    assert isinstance(images, list)
