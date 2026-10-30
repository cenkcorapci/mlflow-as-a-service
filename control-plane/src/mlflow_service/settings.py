"""Configuration is provided by environment variables. No default API key is used."""

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    api_key: str
    database_path: str
    mlflow_url: str

    @classmethod
    def from_env(cls) -> "Settings":
        api_key = os.getenv("CONTROL_API_KEY", "")
        if len(api_key) < 16:
            raise RuntimeError("CONTROL_API_KEY must contain at least 16 characters")
        return cls(
            api_key=api_key,
            database_path=os.getenv("CONTROL_DATABASE_PATH", "/tmp/mlflow-control.db"),
            mlflow_url=os.getenv("CONTROL_MLFLOW_URL", "http://localhost:5000"),
        )
