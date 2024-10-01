"""Utility functions."""

import mlflow
from pydantic import BaseSettings


def set_mlflow_tracking_uri(mlflow_tracking_uri: str):
    """Set MLflow tracking URI."""
    mlflow.set_tracking_uri(mlflow_tracking_uri)
    print(f"MLflow Tracking URI set to: {mlflow_tracking_uri}")


class Envs(BaseSettings):
    """Read env variables."""

    # Declare env vars and assign default values
    mlflow_tracking_uri: str = "http://localhost:8080"
    deploy_model_name: str = "house_price_prediction_prod"
    deploy_model_alias: str = "champion"
    docker_registry: str = "localhost:5000"
    mlflow_built_image_name: str = "mlflow_model"
    mlflow_built_image_tag: str = "latest"

    class Config:
        env_prefix = ""
        case_sensitive = False


envs = Envs()
