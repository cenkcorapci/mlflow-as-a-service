# Execution milestones

These are acceptance criteria, not completed capabilities.

## M0 — local foundation (included in this PR)

- [x] Upstream MLflow tracking + registry server with PostgreSQL metadata and MinIO artifacts
- [x] FastAPI workspace desired-state records (pending only)
- [x] Unit tests and CI definition
- [x] Security boundary, architecture and sample Terraform resource
- [ ] Validate full Docker Compose run and experiment artifact round-trip in CI

## M1 — dedicated workspace reconciler

- [ ] Persistent production database (migrations, transactional idempotency keys)
- [ ] Reconcile pending state to dedicated tenant MLflow server + DB + bucket
- [ ] Safe retries, leases, timeouts, rollback and cleanup
- [ ] Verify client experiment and artifact round-trip before marking ready
- [ ] Tenancy/isolation integration tests on ephemeral deployments

## M2 — secure private beta

- [ ] OIDC, organization roles and secure MLflow authorization path
- [ ] Deployment secrets and cloud IAM with no static root credentials
- [ ] TLS and private endpoint options
- [ ] Audit/metrics/tracing, quotas and billing metering
- [ ] Backup, restore, deletion and migration tests

## M3 — paid pilot

- [ ] Provisioning UX and tenant lifecycle dashboard
- [ ] Usage limits, billing provider, customer support and SLO measurements
- [ ] Two paying design partners; retention and gross-margin validation
- [ ] Explicit SLA and incident-response runbooks

## M4 — expansion

- [ ] GCP/Azure support
- [ ] BYOC workflow and private networking
- [ ] Safe migration tooling and upgrade automation
