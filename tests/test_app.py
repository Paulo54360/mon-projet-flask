import pytest

from src.app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as test_client:
        yield test_client


def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "ok"


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "healthy"


def test_hello(client):
    response = client.get("/hello/Alice")
    assert response.status_code == 200
    assert "Alice" in response.get_json()["message"]


def test_not_found(client):
    response = client.get("/page-inexistante")
    assert response.status_code == 404


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        (3, 5, 8),
        (-1, 1, 0),
        (0, 0, 0),
    ],
)
def test_add(client, a, b, expected):
    response = client.get(f"/add/{a}/{b}")
    assert response.status_code == 200
    assert response.get_json()["result"] == expected


def test_about(client):
    response = client.get("/about")
    assert response.status_code == 200
    data = response.get_json()
    assert data["app"] == "Mon projet Flask"
    assert data["version"] == "1.0"
