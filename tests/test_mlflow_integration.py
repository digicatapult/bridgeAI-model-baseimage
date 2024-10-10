"""MLFlow integration tests."""

import mlflow
import pytest
import requests

from src.utils import set_mlflow_tracking_uri


def test_set_mlflow_tracking_uri():
    """Integration test for MLFlow."""
    mlflow_tracking_uri = "http://localhost:5000"

    # Set the MLflow tracking URI
    set_mlflow_tracking_uri(mlflow_tracking_uri)

    # Verify that the tracking URI is correctly set
    assert mlflow.get_tracking_uri() == mlflow_tracking_uri

    # Verify that the MLflow server is accessible
    try:
        response = requests.get(mlflow_tracking_uri)
        assert (
            response.status_code == 200
        ), f"Failed to access MLflow server at {mlflow_tracking_uri}"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to MLflow server: {e}")
