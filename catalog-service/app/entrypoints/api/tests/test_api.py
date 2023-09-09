from app.entrypoints.api.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_healthz():
    response = client.get("/healthz")
    assert response.status_code == 200


def test_get_products():
    response = client.get("/products")
    assert response.status_code == 200
    assert len(response.json()["products"]) > 0


def test_get_product():
    id = 1
    response = client.get(f"/products/{id}")
    assert response.status_code == 200
    assert response.json()["id"] == id
