"""Build an mlflow deployable docker image."""

import argparse
import os
import subprocess

import mlflow

from src.utils import set_mlflow_tracking_uri


def build_docker_image(model_uri, image_name, use_cli=True):
    """Build mlflow model docker image for deployment."""
    print("MLFLow model docker build starting.")
    if use_cli:
        print("Building using cli...")
        subprocess.run(
            [
                "mlflow",
                "models",
                "build-docker",
                "--model-uri",
                model_uri,
                "--name",
                image_name,
                "--enable-mlserver",
            ],
            check=True,
        )
    else:
        print("Building using python api...")
        mlflow.models.build_docker(
            model_uri=model_uri,
            name=image_name,
            enable_mlserver=True,
            base_image="python:3.12-slim",
        )
    print(f"MLFlow model docker image `{image_name}` build completed.")


def generate_docker_file(
    model_uri: str, out_dir: str = "./mlflow-dockerfile", use_cli: bool = True
):
    """Generate mlflow model Dockerfile for deployment."""
    if use_cli:
        print("Generating Dockerfile using cli...")
        subprocess.run(
            [
                "mlflow",
                "models",
                "generate-dockerfile",
                "--model-uri",
                model_uri,
                "--output-directory",
                out_dir,
                "--enable-mlserver",
            ],
            check=True,
        )
    else:
        print("Generating Dockerfile using python api...")
        raise NotImplementedError

    print(f"MLFlow model Dockerfile generated in `./{out_dir}/`")


def modify_dockerfile(dockerfile_dir: str = "./mlflow-dockerfile/"):
    """Add dependency installation instructions to the dockerfile."""
    # Dependency installation to be added
    install_dependencies = "RUN apt-get -y update && apt-get install " \
                           "-y --no-install-recommends gcc libc-dev\n"

    # Insert the dependency installation line after the FROM line
    dockerfile_path = os.path.join(dockerfile_dir, "Dockerfile")
    with open(dockerfile_path, "r") as file:
        lines = file.readlines()
    for index, line in enumerate(lines):
        if line.startswith("FROM"):
            lines.insert(index + 1, install_dependencies)
            break

    # Update Dockerfile
    with open(dockerfile_path, "w") as file:
        file.writelines(lines)

    print(f"Updated {dockerfile_path} with necessary dependencies.")


def build_from_dockerfile(
    dockerfile_dir: str = "./mlflow-dockerfile/",
    image_name: str = "mlflow_model",
    image_tag: str = "latest",
    use_cli: bool = True,
):
    """Build image from given dockerfile."""
    dockerfile_path = os.path.join(dockerfile_dir, "Dockerfile")
    if use_cli:
        print(
            f"Building image from Dockerfile - {dockerfile_path} using cli..."
        )
        subprocess.run(
            [
                "docker",
                "build",
                "-t",
                f"{image_name}:{image_tag}",
                f"{dockerfile_dir}",
            ],
            check=True,
        )
    else:
        print(
            f"Building image from Dockerfile - "
            f"{dockerfile_path} using python api..."
        )
        raise NotImplementedError


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model_uri",
        type=str,
        required=True,
        help="MLFlow model uri",
    )

    args = parser.parse_args()

    mlflow_tracking_uri = os.getenv(
        "MLFLOW_TRACKING_URI", "http://mlflow-tracking:80"
    )
    set_mlflow_tracking_uri(mlflow_tracking_uri)

    model_uri = args.model_uri

    model_docker_image_name = os.getenv(
        "MODEL_DOCKER_IMAGE", "house_price_model"
    )
    mlflow_build_base_image = os.getenv(
        "MODEL_DOCKER_IMAGE", "python:3.12.4-slim"
    )

    build_docker_image(
        model_uri, model_docker_image_name, mlflow_build_base_image
    )
