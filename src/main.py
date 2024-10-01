"""Main entry point."""

from src.build_mlflow_docker_image import (build_from_dockerfile,
                                           generate_docker_file,
                                           modify_dockerfile)
from src.get_mlflow_model_details import get_model_run_uri
from src.push_image_to_cr import push_image_to_docker_registry
from src.utils import envs, set_mlflow_tracking_uri

if __name__ == "__main__":

    # Set the output directory for docker files and artefacts
    out_dir = "./mlflow-dockerfile"

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
    modify_dockerfile(dockerfile_dir=out_dir)

    # Build docker image to be used as the base image for deployment
    docker_image = build_from_dockerfile(
        image_name=envs.mlflow_built_image_name,
        docker_registry=envs.docker_registry,
        image_tag=envs.mlflow_built_image_tag,
    )

    # Push the built image to local container registry
    push_image_to_docker_registry(docker_image)
