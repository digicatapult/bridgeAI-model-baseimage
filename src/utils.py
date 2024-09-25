"""Utility functions."""

import mlflow


def set_mlflow_tracking_uri(mlflow_tracking_uri: str):
    """Set MLflow tracking URI."""
    mlflow.set_tracking_uri(mlflow_tracking_uri)
    print(f"MLflow Tracking URI set to: {mlflow_tracking_uri}")
