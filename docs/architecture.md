# Architecture and tenancy boundaries

## Today: runnable local developer stack

```text
Developer machine (localhost-only ports)
+----------------------+                  +-----------------------------+
| Control API          |                  | MLflow server (upstream)    |
| FastAPI + SQLite     |--health probe--->| HTTP tracking/registry API  |
| workspace intent DB  |                  +-------------+---------------+
| status = pending     |                                |
+----------------------+                       +--------+---------+
                                               |                  |
                                           PostgreSQL          MinIO (S3)
                                           metadata           artifacts
```

The control plane's `POST /v1/workspaces` **only records an intent** and never launches an MLflow instance. One shared local MLflow installation is offered for smoke testing; it is **not** used to isolate workspace records.

## Target: commercial service (not implemented)

```text
GitHub/Google/enterprise OIDC -> SaaS console / API
                                     |
                           control-plane database
                                     |
                         reconciler + state machine
                                     |
                    Terraform / Kubernetes deployment
                                     |
              +----------------------+----------------------+
              |                      |                      |
          Tenant A                Tenant B              Tenant C
          MLflow pod              MLflow pod            BYOC (future)
          DB/schema *             DB/schema *           customer account
          Artifact bucket         Artifact bucket
          IAM principal           IAM principal
          private ingress         private ingress
```

*Prefer physically separate databases for the dedicated tier; schema isolation can be acceptable only with rigorous threat analysis, credentials, tested backup/restore and privilege boundaries.

## Provisioning state machine (proposed)

`pending -> provisioning -> ready`, with `failed`, `upgrading`, `suspended`, `deleting` and `deleted` states added by a real reconciler. Every operation must be idempotent, retry-safe, lease-protected, audited, and observable. Never claim `ready` from an API write alone; verify the endpoint, database migrations, and artifact round-trip.

## Provider strategy

- **Phase 1:** single cloud region, managed dedicated workspace per customer, one MLflow API endpoint, customer-specific Postgres and object storage.
- **Phase 2:** automated deployments, lifecycle and metering, SSO, billing, backup and restore.
- **Phase 3:** other cloud providers, BYOC and private networking, migration tooling.

Do not use MLflow experiments, tags, or workspaces as a tenant security boundary. Upstream MLflow is compatible with this architecture, but isolation, identity, logging, policy enforcement and abuse controls are platform obligations.
