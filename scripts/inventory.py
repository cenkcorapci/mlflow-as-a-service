"""Read-only inventory of an existing MLflow server for migration planning.

Requires: pip install mlflow==3.17.2
Uses the standard MLFLOW_TRACKING_URI and MLflow auth environment variables.
No source mutations, copying or ID preservation are attempted.
"""

import json
import os

from mlflow import MlflowClient
from mlflow.entities import ViewType


def main() -> None:
    if not os.getenv("MLFLOW_TRACKING_URI"):
        raise SystemExit("Set MLFLOW_TRACKING_URI to the source server before running.")
    client = MlflowClient()
    experiments = client.search_experiments(view_type=ViewType.ALL)
    output = [
        {
            "experiment_id": experiment.experiment_id,
            "name": experiment.name,
            "lifecycle_stage": experiment.lifecycle_stage,
            "artifact_location": experiment.artifact_location,
        }
        for experiment in experiments
    ]
    print(json.dumps({"experiments": output}, indent=2))


if __name__ == "__main__":
    main()
