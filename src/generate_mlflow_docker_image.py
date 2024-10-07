"""Generate Dockerfile to create deployable mlflow model base image."""

import argparse
import os

from mlflow.pyfunc.backend import PyFuncBackend

from src.utils import envs, set_mlflow_tracking_uri


def generate_docker_file(model_uri: str, out_dir: str = "./mlflow-dockerfile"):
    """Generate mlflow model Dockerfile for deployment."""
    print("Generating Dockerfile using python api...")
    # Create an instance of the PyFuncBackend class
    backend = PyFuncBackend(config={}, env_manager="conda")
    backend.generate_dockerfile(
        model_uri=model_uri, output_dir=out_dir, enable_mlserver=True
    )

    print(f"MLFlow model Dockerfile generated in `./{out_dir}/`")


def update_dockerfile(
    dockerfile_dir: str = "./mlflow-dockerfile/", command: str = ""
):
    """Add dependency installation instructions to the dockerfile."""
    # Command to install dependencies
    if command == "":
        command_to_install_deps = (
            "RUN apt-get -y update && apt-get install "
            "-y --no-install-recommends gcc libc-dev\n"
        )
    else:
        command_to_install_deps = command

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
    update_dockerfile(dockerfile_dir=args.out_dir)
