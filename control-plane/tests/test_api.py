import tempfile
from pathlib import Path

from fastapi.testclient import TestClient

from mlflow_service.api import make_app
from mlflow_service.settings import Settings


def client():
    directory = tempfile.TemporaryDirectory()
    app = make_app(
        Settings(
            api_key="test-key-at-least-16-characters",
            database_path=str(Path(directory.name) / "control.db"),
            mlflow_url="http://127.0.0.1:59999",
        )
    )
    return directory, TestClient(app)


def test_health_and_authentication():
    directory, test_client = client()
    with directory, test_client as c:
        assert c.get("/healthz").json()["status"] == "ok"
        assert c.get("/v1/workspaces").status_code == 401
        assert c.get("/v1/workspaces", headers={"X-API-Key": "incorrect"}).status_code == 401


def test_workspace_lifecycle_is_pending_without_provisioning():
    directory, test_client = client()
    headers = {"X-API-Key": "test-key-at-least-16-characters"}
    with directory, test_client as c:
        payload = {"name": "Example Team", "slug": "example-team"}
        response = c.post("/v1/workspaces", json=payload, headers=headers)
        assert response.status_code == 201
        workspace = response.json()
        assert workspace["status"] == "pending"
        assert workspace["deployment_mode"] == "dedicated"
        assert c.post("/v1/workspaces", json=payload, headers=headers).status_code == 409
        assert c.get("/v1/workspaces/example-team", headers=headers).json()["id"] == workspace["id"]
        assert len(c.get("/v1/workspaces", headers=headers).json()) == 1
        assert c.get("/v1/workspaces/unknown", headers=headers).status_code == 404


def test_workspace_validation_and_mlflow_probe():
    directory, test_client = client()
    headers = {"X-API-Key": "test-key-at-least-16-characters"}
    with directory, test_client as c:
        bad = c.post("/v1/workspaces", json={"name": "X", "slug": "../bad"}, headers=headers)
        assert bad.status_code == 422
        probe = c.get("/v1/local-mlflow", headers=headers)
        assert probe.status_code == 200
        assert probe.json()["reachable"] is False
