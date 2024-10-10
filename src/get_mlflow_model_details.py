"""Gather required model and run details of the model we want to deploy."""

import json

from src.utils import envs, set_mlflow_tracking_uri


def get_model_run_uri(model_name: str, model_alias: str):
    """Create an accessible mlflow model uri."""
    model_uri = f"models:/{model_name}@{model_alias}"
    print(f"MLflow model URI: {model_uri}")

    return model_uri


if __name__ == "__main__":
    set_mlflow_tracking_uri(envs.mlflow_tracking_uri)
    model_uri = get_model_run_uri(
        envs.deploy_model_name, envs.deploy_model_alias
    )

    # write model_uri to the file checked by Airflow for task XComs
    xcom_json = {"model_uri": f"{model_uri}"}

    with open("/airflow/xcom/return.json", "w") as f:
        json.dump(xcom_json, f)
