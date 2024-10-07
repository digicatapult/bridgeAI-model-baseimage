from unittest import mock

import pytest

from src.generate_mlflow_docker_image import (
    generate_docker_file,
    update_dockerfile,
)


@pytest.fixture
def mock_pyfunc_backend():
    with mock.patch(
        "src.generate_mlflow_docker_image.PyFuncBackend"
    ) as MockBackend:
        yield MockBackend


def test_generate_docker_file(mock_pyfunc_backend, tmp_path):
    model_uri = "fake_model_uri"
    output_dir = tmp_path / "mlflow-dockerfile"

    # Mock backend instance
    mock_backend_instance = mock_pyfunc_backend.return_value

    generate_docker_file(model_uri, out_dir=str(output_dir))

    # Verify that the backend's `generate_dockerfile` method
    # was called with the correct parameters
    mock_backend_instance.generate_dockerfile.assert_called_once_with(
        model_uri=model_uri, output_dir=str(output_dir), enable_mlserver=True
    )


def test_update_dockerfile(tmp_path):
    # Prepare a mock Dockerfile for testing
    dockerfile_dir = tmp_path / "mlflow-dockerfile"
    dockerfile_dir.mkdir(parents=True, exist_ok=True)
    dockerfile_path = dockerfile_dir / "Dockerfile"
    with open(dockerfile_path, "w") as dockerfile:
        dockerfile.write("FROM python:3.12\n")

    update_dockerfile(dockerfile_dir=str(dockerfile_dir))

    # Verify that the Dockerfile was updated correctly
    with open(dockerfile_path, "r") as dockerfile:
        lines = dockerfile.readlines()

    assert "FROM python:3.12\n" in lines
    assert (
        "RUN apt-get -y update && apt-get install -y "
        "--no-install-recommends gcc libc-dev\n" in lines
    )
