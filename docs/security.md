# Security boundary and production blockers

**Never deploy docker-compose.yml to a public host.** It exposes MLflow and MinIO over plain HTTP without MLflow login; the control API uses a shared static API key. Every published port is bound to `127.0.0.1` for local use only. The MinIO root user is not a production IAM identity. Local secrets live in an ignored `.env`; change defaults before starting.

## What is implemented

- API key checked with constant-time comparison on workspace routes.
- Explicit validation of workspace slug and deployment mode.
- Local-only published ports.
- Separate Postgres and S3-compatible artifact services for correct MLflow semantics.
- Control-plane and MLflow metadata kept in different data stores.

## What must be delivered before external beta

1. OIDC login, organizations and project-level RBAC; tenant-scoped tokens with rotation/revocation; auth at **every** MLflow endpoint.
2. Dedicated network, process, Postgres and artifact-bucket isolation. No shared MLflow backend with a tag-based tenancy scheme.
3. TLS, least-privilege workload identity, KMS encryption, bucket policies, egress policy, private endpoints and secret management.
4. Complete audit trail, quota/rate limiting, safe artifact upload/download checks, malware/abuse controls, bounded request sizes.
5. Lifecycle reconciliation, database migrations, restore drills, retention, deletion guarantees and data residency.
6. Dependency/image pinning by digest, SBOM, CI scanning, third-party security review and incident response.
7. Threat model for arbitrary model/artifact serialization; never execute untrusted customer models on the control plane.

**Critical limitation:** `/v1/workspaces` metadata is not linked to MLflow access control. It cannot be used as a SaaS tenant registry yet. Do not onboard untrusted customers.

## Secrets and data

No credentials in Git, CI logs or PRs. `.env` is ignored. Production tokens must be tenant-scoped and never returned in API list responses. Use vault/KMS in production; audit both control plane actions and data plane changes.
