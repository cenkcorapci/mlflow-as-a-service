"""Log a simple experiment and artifact via the standard upstream MLflow client."""

import os

import mlflow


def main() -> None:
    mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000"))
    mlflow.set_experiment("mvp-smoke-test")
    with mlflow.start_run(run_name="hello-managed-mlflow"):
        mlflow.log_param("algorithm", "baseline")
        mlflow.log_param("data_source", "synthetic")
        mlflow.log_metric("accuracy", 0.91)
        mlflow.log_text("This artifact is stored in MinIO via the MLflow server.\n", "notes.txt")
        print("Run ID:", mlflow.active_run().info.run_id)


if __name__ == "__main__":
    main()
