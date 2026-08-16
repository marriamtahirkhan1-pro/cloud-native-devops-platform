from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == "Cloud Native DevOps Platform API"


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_create_task():
    response = client.post(
        "/api/tasks",
        json={
            "title": "Test Task",
            "description": "Testing API",
            "completed": False
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "Test Task"
    assert data["completed"] is False


def test_get_tasks():
    response = client.get("/api/tasks")

    assert response.status_code == 200
    assert isinstance(response.json(), list)