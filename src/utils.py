"""Utility functions."""

import mlflow
from pydantic_settings import BaseSettings, SettingsConfigDict


def set_mlflow_tracking_uri(mlflow_tracking_uri: str):
    """Set MLflow tracking URI."""
    mlflow.set_tracking_uri(mlflow_tracking_uri)
    print(f"MLflow Tracking URI set to: {mlflow_tracking_uri}")


class Envs(BaseSettings):
    """Read env variables."""

    # Declare env vars and assign default values
    mlflow_tracking_uri: str = "https://mlflow.dc-mlops.co.uk"
    deploy_model_name: str = "house_price_prediction_prod"
    deploy_model_alias: str = "champion"
    mlflow_docker_out_dir: str = "./mlflow-dockerfile"
    mlflow_tracking_username: str | None = None
    mlflow_tracking_password: str | None = None

    model_config = SettingsConfigDict(env_prefix="", case_sensitive=False)


envs = Envs()
