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


def test_create_and_get_product(auth_headers):
    # 1. Create product
    prod_payload = {
        "product_name": "Organic Green Tea",
        "brand": "Pure Leaf",
        "category": "Beverages",
        "manufacturer": "Pure Leaf Plantation Ltd., Assam",
        "batch_number": "GT-2026-01",
    }
    create_resp = client.post("/api/products", json=prod_payload, headers=auth_headers)
    assert create_resp.status_code == 201
    prod_data = create_resp.json()
    assert prod_data["product_name"] == "Organic Green Tea"
    assert "id" in prod_data
    prod_id = prod_data["id"]

    # 2. Get product by ID
    get_resp = client.get(f"/api/products/{prod_id}", headers=auth_headers)
    assert get_resp.status_code == 200
    assert get_resp.json()["id"] == prod_id


def test_search_and_list_products(auth_headers):
    # Search
    search_resp = client.get("/api/products/search?q=Biscuits", headers=auth_headers)
    assert search_resp.status_code == 200
    results = search_resp.json()
    assert isinstance(results, list)
    assert any("Biscuits" in p["product_name"] for p in results)

    # Paginated List
    list_resp = client.get("/api/products?page=1&limit=5", headers=auth_headers)
    assert list_resp.status_code == 200
    data = list_resp.json()
    assert "items" in data
    assert "total" in data
    assert "total_pages" in data
    assert data["page"] == 1


def test_create_inspection_generates_id(auth_headers):
    insp_payload = {
        "product_name": "Sunflower Cooking Oil 1L",
        "brand": "Golden Sun",
        "category": "Edible Oils",
        "manufacturer": "Sun Agro Ltd., Gujarat",
        "batch_number": "SO-882",
        "location": "Vashi APMC Market, Navi Mumbai",
    }
    response = client.post("/api/inspections", json=insp_payload, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["inspection_id"].startswith("LM-")
    assert data["status"] == "DRAFT"
    assert data["compliance_score"] == 0.0
    assert data["product"]["product_name"] == "Sunflower Cooking Oil 1L"


def test_list_and_filter_inspections(auth_headers):
    # Filter by search
    resp = client.get("/api/inspections?search=Biscuits", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] >= 1
    assert any("Biscuits" in item["product"]["product_name"] for item in data["items"])

    # Filter by status
    resp_status = client.get("/api/inspections?status=REQUIRES_REVIEW", headers=auth_headers)
    assert resp_status.status_code == 200
    assert resp_status.json()["total"] >= 1


def test_get_inspection_detail_and_update(auth_headers):
    # Get seeded inspection LM-2026-0248
    get_resp = client.get("/api/inspections/LM-2026-0248", headers=auth_headers)
    assert get_resp.status_code == 200
    data = get_resp.json()
    assert data["inspection_id"] == "LM-2026-0248"
    assert "declarations" in data
    assert "violations" in data

    # Update inspection
    update_resp = client.put(
        "/api/inspections/LM-2026-0248",
        json={"location": "Bandra Retail Store, Mumbai"},
        headers=auth_headers,
    )
    assert update_resp.status_code == 200
    assert update_resp.json()["location"] == "Bandra Retail Store, Mumbai"
