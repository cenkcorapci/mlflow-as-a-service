"""Local-only provisioning *intent* API; real provisioning is not implemented."""

import secrets
import sqlite3
import uuid
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import Annotated, Literal

import httpx
from fastapi import Depends, FastAPI, Header, HTTPException, status
from pydantic import BaseModel, Field

from mlflow_service.settings import Settings
from mlflow_service.storage import find_all, find_by_slug, initialize, insert_workspace


class WorkspaceCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    slug: str = Field(pattern=r"^[a-z][a-z0-9-]{2,38}[a-z0-9]$", max_length=40)
    deployment_mode: Literal["dedicated"] = "dedicated"


class Workspace(WorkspaceCreate):
    id: str
    status: Literal["pending"]
    created_at: str


def make_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or Settings.from_env()

    @asynccontextmanager
    async def lifespan(_: FastAPI):
        initialize(settings.database_path)
        yield

    app = FastAPI(
        title="Managed MLflow Control Plane",
        version="0.1.0",
        description="Developer prototype. Records intent; does not provision a tenant.",
        lifespan=lifespan,
    )

    def authenticate(x_api_key: Annotated[str | None, Header()] = None) -> None:
        if x_api_key is None or not secrets.compare_digest(x_api_key, settings.api_key):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    Auth = Annotated[None, Depends(authenticate)]

    @app.get("/healthz")
    def healthz():
        return {"status": "ok", "component": "control-plane"}

    @app.get("/v1/local-mlflow", dependencies=[Depends(authenticate)])
    async def local_mlflow():
        try:
            async with httpx.AsyncClient(timeout=3.0, follow_redirects=False) as client:
                response = await client.get(f"{settings.mlflow_url.rstrip('/')}/health")
            return {
                "reachable": response.status_code == 200,
                "http_status": response.status_code,
            }
        except httpx.RequestError:
            return {"reachable": False, "http_status": None}

    @app.post("/v1/workspaces", response_model=Workspace, status_code=201)
    def create_workspace(payload: WorkspaceCreate, _auth: Auth):
        workspace = {
            **payload.model_dump(),
            "id": str(uuid.uuid4()),
            "status": "pending",
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        try:
            created = insert_workspace(settings.database_path, workspace)
        except sqlite3.OperationalError as exc:
            raise HTTPException(status_code=503, detail="Storage unavailable") from exc
        if not created:
            raise HTTPException(status_code=409, detail="Workspace slug already exists")
        return workspace

    @app.get("/v1/workspaces", response_model=list[Workspace])
    def list_workspaces(_auth: Auth):
        return find_all(settings.database_path)

    @app.get("/v1/workspaces/{slug}", response_model=Workspace)
    def get_workspace(slug: str, _auth: Auth):
        workspace = find_by_slug(settings.database_path, slug)
        if workspace is None:
            raise HTTPException(status_code=404, detail="Workspace not found")
        return workspace

    return app


# Container startup evaluates environment; tests use make_app(injected_settings).
app = make_app()
