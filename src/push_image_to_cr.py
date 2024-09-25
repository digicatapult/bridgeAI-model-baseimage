"""Push the docker image created to container registry."""

import os
import subprocess

import docker

dockerhub_username = os.getenv("DOCKERHUB_USERNAME")
dockerhub_password = os.getenv("DOCKERHUB_PASSWORD")


def push_image_to_dockerhub(
    image_name: str, image_tag: str = "latest", use_cli: bool = True
):
    """Push the docker image to docker hub."""
    image_full_name = f"{dockerhub_username}/{image_name}:{image_tag}"

    if use_cli:
        try:
            # TODO: change this temporary authentication method
            subprocess.run(
                [
                    "docker",
                    "login",
                    "--username",
                    dockerhub_username,
                    "--password",
                    dockerhub_password,
                ],
                check=True,
            )

            subprocess.run(
                [
                    "docker",
                    "tag",
                    f"{image_name}:{image_tag}",
                    image_full_name,
                ],
                check=True,
            )

            print(
                f"Pushing image {image_full_name} to docker hub using Docker CLI..."
            )
            subprocess.run(["docker", "push", image_full_name], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error pushing image to docker hub: {e}")
            raise
    else:
        try:
            # TODO: test and correct this method and make this default
            client = docker.from_env()
            print(
                f"Pushing image {image_full_name} to docker hub using python api..."
            )
            client.images.push(image_name, tag=image_tag)
        except docker.errors.APIError as e:
            print(f"Error pushing image to docker hub: {e}")
            raise
    print(f"Successfully pushed {image_full_name} to Docker Hub.")
