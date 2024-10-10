"""Main entry point."""

from src.generate_mlflow_docker_image import (
    generate_docker_file,
    update_dockerfile,
)
from src.get_mlflow_model_details import get_model_run_uri
from src.utils import envs, set_mlflow_tracking_uri

if __name__ == "__main__":

    # Set the output directory for docker files and artefacts
    out_dir = envs.mlflow_docker_out_dir

    # Set the mlflow tracking uri before getting the model details
    set_mlflow_tracking_uri(envs.mlflow_tracking_uri)

    # Get the model uri;
    # to collect the model and artefacts form the mlflow remote registry
    model_uri = get_model_run_uri(
        envs.deploy_model_name, envs.deploy_model_alias
    )

    # Generate a docker file with artefacts and dependencies gathered
    # from the mlflow remote registry
    generate_docker_file(model_uri, out_dir=out_dir)

    # Add missing dependencies to the generated dockerfile
    update_dockerfile(dockerfile_dir=out_dir)
