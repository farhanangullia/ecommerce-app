from app.entrypoints.api.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_healthz():
    response = client.get("/healthz")
    assert response.status_code == 200


def test_new_session():
    response = client.post("/cart/session")
    assert response.status_code == 200
    assert response.headers["x-session-id"]


def test_get_cart():
    response = client.get("/cart", headers={"X-Session-ID": "abc"})
    assert response.status_code == 200
    assert type(response.json()["items"]) == list
