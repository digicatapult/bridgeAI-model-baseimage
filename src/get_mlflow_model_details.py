"""Gather required model and run details of the model we want to deploy."""

import json
import os

from src.utils import set_mlflow_tracking_uri


def get_model_run_uri(
    mlflow_tracking_uri: str, model_name: str, model_alias: str
):
    """Create an accessible mlflow model uri."""
    model_uri = f"models:/{model_name}@{model_alias}"
    print(f"MLflow model URI: {model_uri}")

    return model_uri


if __name__ == "__main__":
    mlflow_tracking_uri = os.getenv(
        "MLFLOW_TRACKING_URI", "http://mlflow-tracking:80"
    )
    model_name = os.getenv("DEPLOY_MODEL_NAME", "house_price_prediction_prod")
    model_alias = os.getenv("DEPLOY_MODEL_ALIAS", "champion")

    set_mlflow_tracking_uri(mlflow_tracking_uri)
    model_uri = get_model_run_uri(mlflow_tracking_uri, model_name, model_alias)

    # write to the file checked by Airflow for XComs
    xcom_json = {"model_uri": f"{model_uri}"}

    with open("/airflow/xcom/return.json", "w") as f:
        json.dump(xcom_json, f)
