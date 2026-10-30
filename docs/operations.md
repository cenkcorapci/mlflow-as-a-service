# Local operations runbook

1. Copy `.env.example` to `.env`; replace every sample password/token.
2. Run `docker compose config` to validate configuration, then `docker compose up --build -d`.
3. Check `docker compose ps`. The MLflow server becomes healthy after its metadata schema initializes.
4. Run `python examples/log_run.py` with an installed MLflow client and `MLFLOW_TRACKING_URI=http://localhost:5000`. Validate parameters and artifact in the UI.
5. Call `/healthz` and `/v1/local-mlflow`. Creating a workspace should remain **pending**.
6. For errors inspect `docker compose logs --tail=200 postgres minio minio-init mlflow control-plane`.

## Caveats

- A MinIO/MLflow restart can take longer on first startup. Never use this stack for customer traffic.
- Persistent Docker volumes hold experiment metadata and artifacts. `docker compose down -v` destroys them.
- `infra/terraform/aws-artifacts` is only a bucket example, not a provisioned stack, and carries cloud charges if applied.
- Do not promise data restoration until backup snapshots and a full restore drill exist.

## Upgrade path

Pin exact image digests, add migrations and backups, test version compatibility, stage a canary tenant, then roll out gradually. All of these are future production tasks.
