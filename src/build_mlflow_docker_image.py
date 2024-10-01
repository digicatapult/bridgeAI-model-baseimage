"""Build an mlflow deployable docker image."""

import argparse
import json
import os

import docker
from mlflow.pyfunc.backend import PyFuncBackend

from src.utils import envs, set_mlflow_tracking_uri


def generate_docker_file(model_uri: str, out_dir: str = "./mlflow-dockerfile"):
    """Generate mlflow model Dockerfile for deployment."""
    print("Generating Dockerfile using python api...")
    config = {}
    env_manager = "conda"
    # Create an instance of the PyFuncBackend class
    backend = PyFuncBackend(config=config, env_manager=env_manager)
    # backend = PyFuncBackend()
    backend.generate_dockerfile(
        model_uri=model_uri, output_dir=out_dir, enable_mlserver=True
    )

    print(f"MLFlow model Dockerfile generated in `./{out_dir}/`")


def modify_dockerfile(dockerfile_dir: str = "./mlflow-dockerfile/"):
    """Add dependency installation instructions to the dockerfile."""
    # Command to install dependencies
    command_to_install_deps = (
        "RUN apt-get -y update && apt-get install "
        "-y --no-install-recommends gcc libc-dev\n"
    )

    # Insert the dependency installation line after the FROM line
    dockerfile_path = os.path.join(dockerfile_dir, "Dockerfile")
    with open(dockerfile_path, "r") as file:
        lines = file.readlines()
    for index, line in enumerate(lines):
        if line.startswith("FROM"):
            lines.insert(index + 1, command_to_install_deps)
            break

    # Update Dockerfile
    with open(dockerfile_path, "w") as file:
        file.writelines(lines)

    print(f"Updated {dockerfile_path} with necessary dependencies.")


def build_from_dockerfile(
    dockerfile_dir: str = "./mlflow-dockerfile/",
    docker_registry: str = "localhost:5000",
    image_name: str = "mlflow_model",
    image_tag: str = "latest",
):
    """Build image from given dockerfile."""
    dockerfile_path = os.path.join(dockerfile_dir, "Dockerfile")

    print(
        f"Building image from Dockerfile - "
        f"{dockerfile_path} using python api..."
    )

    try:
        client = docker.from_env()
        full_image_name = f"{docker_registry}/{image_name}:{image_tag}"

        # Build the Docker image
        print(
            f"Building Docker image {full_image_name} from {dockerfile_dir}..."
        )
        image, logs = client.images.build(
            path=dockerfile_dir, tag=full_image_name
        )

        # Print build logs
        for log in logs:
            if "stream" in log:
                print(log["stream"].strip())

        print(f"Docker image {full_image_name} built successfully!")
    except docker.errors.BuildError as e:
        print(f"Error building Docker image: {str(e)}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

    return full_image_name


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model_uri",
        type=str,
        required=True,
        help="MLFlow model uri",
    )

    parser.add_argument(
        "--out_dir", type=str, required=False, default="./mlflow-dockerfile"
    )

    args = parser.parse_args()

    set_mlflow_tracking_uri(envs.mlflow_tracking_uri)

    model_uri = args.model_uri

    # Generate a docker file with artefacts and dependencies gathered
    # from the mlflow remote registry
    generate_docker_file(model_uri, out_dir=args.out_dir)

    # Add missing dependencies to the generated dockerfile
    modify_dockerfile(dockerfile_dir=args.out_dir)

    # Build docker image to be used as the base image for deployment
    docker_image = build_from_dockerfile(
        image_name=envs.mlflow_built_image_name,
        docker_registry=envs.docker_registry,
        image_tag=envs.mlflow_built_image_tag,
    )

    # write model_uri to the file checked by Airflow for task XComs
    xcom_json = {"docker_image": f"{docker_image}"}

    with open("/airflow/xcom/return.json", "w") as f:
        json.dump(xcom_json, f)
