# Product hypothesis and commercial assumptions

**Working hypothesis, not validated market research:** teams running MLflow themselves have material operational pain around identity, upgrades, high availability, backups and portability. Managed MLflow alone competes with Databricks and native cloud platforms. Customer-funded willingness to pay must be tested before building a complete platform.

## ICP

First focus on 10–100 person ML/AI teams that have existing MLflow clients, do not want a bundled compute platform, and need a portable tracking + registry service. Exclude buyers who simply want a free managed-tier add-on.

## Product promise

1. Standard `MLFLOW_TRACKING_URI` and existing MLflow clients work unmodified.
2. Data plane dedicated per tenant, with a documented security boundary.
3. One-click provisioning/upgrade/backups **only when proven by automation**.
4. Safe migration from self-hosted tracking (IDs/artifact paths and permissions require design work).
5. Transparent storage/egress and clearly priced compute.

## Positioning to validate

- **Control vs convenience:** dedicated cloud account / BYOC as premium tier.
- **Cost vs DIY:** time saved on maintenance, not arbitrary low SaaS price.
- **Neutrality:** do not require adopting proprietary orchestration/training infrastructure.

## Pricing experiments (hypothetical, not a forecast)

Interview customers with three packaging anchors: hobby sandbox, dedicated small-team, and enterprise/private deployment. Price based on workspace isolation, service tier and included retention/storage; pass through variable storage/egress. Validate monthly willingness to pay, not stated enthusiasm.

## Kill criteria

Stop or pivot after 15–20 ICP interviews if teams will not commit to a pilot, cannot identify a budget owner, or demand multi-cloud/SSO/SLA features beyond viable unit economics. Do not infer TAM from MLflow GitHub stars.
