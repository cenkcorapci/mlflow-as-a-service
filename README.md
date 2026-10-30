# MLflow as a Service

**Production-grade MLflow everywhere.** A cloud-neutral managed MLflow product prototype, building on upstream MLflow rather than forking it.

> **Status: engineering MVP foundation / local development only.** This repository does **not** yet deliver production SaaS, tenant provisioning, user authentication for MLflow, private networking, BYOC, automatic backups, or contractual SLAs. See [security](docs/security.md) and [roadmap](docs/roadmap.md).

## Thesis

Managed tracking alone is commoditised. The differentiation is deployment portability, **dedicated tenant data planes**, frictionless migration, secure identity, upgrades and recovery. See [product strategy](docs/product.md).

## What works now

- A locally runnable **upstream MLflow** tracking + model registry server with **PostgreSQL** metadata and **MinIO** S3-compatible artifact storage.
- A **FastAPI control-plane prototype** with API-key-gated workspace desired-state registration, readiness checks and a local MLflow probe. Creating a workspace **does not yet provision a data plane**.
- A Python MLflow logging example, basic API tests, CI, an AWS artifact-bucket Terraform example, and architecture/operations documents.

## Quick start

Requires Docker Compose v2, Python 3.12+ for the example.

```bash
cp .env.example .env
# Replace CONTROL_API_KEY, POSTGRES_PASSWORD and MINIO_ROOT_PASSWORD with local secrets.
docker compose up --build -d
docker compose ps

# MLflow UI: http://localhost:5000
# Control-plane OpenAPI: http://localhost:8000/docs
# MinIO console: http://localhost:9001

python -m pip install "mlflow==3.17.2"
MLFLOW_TRACKING_URI=http://localhost:5000 python examples/log_run.py
```

The MinIO init job creates the `mlflow-artifacts` bucket. Logs:

```bash
docker compose logs -f mlflow control-plane
```

Create a **desired-state record** (it remains `pending`; there is no reconciler yet):

```bash
set -a; . ./.env; set +a
curl -s -X POST http://localhost:8000/v1/workspaces \
  -H "X-API-Key: $CONTROL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name":"Example team","slug":"example-team","deployment_mode":"dedicated"}'
```

Check the local server:

```bash
curl -s http://localhost:8000/healthz
curl -s -H "X-API-Key: $CONTROL_API_KEY" http://localhost:8000/v1/local-mlflow
```

Stop the stack: `docker compose down`. **Destructive:** `docker compose down -v` removes all local experiment metadata and artifacts.

## Repository map

| Path | Purpose |
|---|---|
| `control-plane/` | FastAPI prototype, SQLite desired-state repository, tests |
| `docker/` | Container build definitions |
| `docker-compose.yml` | Developer-only stack: MLflow, PostgreSQL, MinIO, API |
| `examples/` | Upstream client compatibility smoke test |
| `scripts/` | Existing MLflow server inventory (read-only) |
| `infra/terraform/aws-artifacts/` | Example AWS S3 bucket only; not a full deployment |
| `docs/` | Architecture, security, operations, strategy, milestones |
| `.github/workflows/` | Lint and unit-test workflow |

## Developing the control plane

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e './control-plane[dev]'
ruff check control-plane
ruff format --check control-plane
pytest control-plane/tests
```

See [architecture](docs/architecture.md), [roadmap](docs/roadmap.md), [operations](docs/operations.md), and [security](docs/security.md).

## Design principles

1. **Upstream MLflow compatibility.** No proprietary training SDK required.
2. **Isolation is a deployment boundary.** MLflow workspaces are not hard tenant isolation.
3. **Control-plane/data-plane separation.** Data, metadata and customer secrets stay in dedicated data planes in paid production tiers.
4. **Portability first.** AWS, Azure, GCP and eventually BYOC/on-prem.
5. **Explicit status.** A pending provisioning record is not a deployed workspace.

**License:** MIT for this repository's original code. MLflow and other dependencies retain their own licenses.
