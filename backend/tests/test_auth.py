import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.config import settings

client = TestClient(app)


def test_login_success_admin():
    response = client.post(
        "/api/auth/login",
        json={
            "email": settings.SEED_ADMIN_EMAIL,
            "password": settings.SEED_ADMIN_PASSWORD,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["user"]["email"] == settings.SEED_ADMIN_EMAIL
    assert data["user"]["role"] == "ADMIN"


def test_login_success_inspector():
    response = client.post(
        "/api/auth/login",
        json={
            "email": settings.SEED_INSPECTOR_EMAIL,
            "password": settings.SEED_INSPECTOR_PASSWORD,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["user"]["role"] == "INSPECTOR"


def test_login_invalid_password():
    response = client.post(
        "/api/auth/login",
        json={
            "email": settings.SEED_ADMIN_EMAIL,
            "password": "WrongPassword123!",
        },
    )
    assert response.status_code == 401
    data = response.json()
    assert "error" in data
    assert data["error"]["code"] == "INVALID_CREDENTIALS"


def test_get_me_authenticated():
    # Login to get token
    login_resp = client.post(
        "/api/auth/login",
        json={
            "email": settings.SEED_INSPECTOR_EMAIL,
            "password": settings.SEED_INSPECTOR_PASSWORD,
        },
    )
    token = login_resp.json()["access_token"]

    # Call /api/auth/me
    response = client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    user_data = response.json()
    assert user_data["email"] == settings.SEED_INSPECTOR_EMAIL
    assert user_data["role"] == "INSPECTOR"


def test_get_me_unauthenticated():
    response = client.get("/api/auth/me")
    assert response.status_code == 401


def test_admin_rbac_protection():
    # 1. Inspector token should fail accessing admin-only /api/users
    insp_login = client.post(
        "/api/auth/login",
        json={
            "email": settings.SEED_INSPECTOR_EMAIL,
            "password": settings.SEED_INSPECTOR_PASSWORD,
        },
    )
    insp_token = insp_login.json()["access_token"]
    resp_forbidden = client.get(
        "/api/users",
        headers={"Authorization": f"Bearer {insp_token}"},
    )
    assert resp_forbidden.status_code == 403
    assert resp_forbidden.json()["error"]["code"] == "FORBIDDEN"

    # 2. Admin token should succeed accessing /api/users
    admin_login = client.post(
        "/api/auth/login",
        json={
            "email": settings.SEED_ADMIN_EMAIL,
            "password": settings.SEED_ADMIN_PASSWORD,
        },
    )
    admin_token = admin_login.json()["access_token"]
    resp_admin = client.get(
        "/api/users",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert resp_admin.status_code == 200
    assert isinstance(resp_admin.json(), list)
    assert len(resp_admin.json()) >= 2
