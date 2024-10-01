"""Push the docker image created to container registry."""

import argparse

import docker


def push_image_to_docker_registry(image_full_name: str):
    """Push the docker image to docker hub."""
    try:
        client = docker.from_env()
        print(f"Pushing {image_full_name} to docker hub using python api...")
        push_logs = client.images.push(image_full_name)
        for log in push_logs:
            # Getting rid of 'pushing' progress status logs
            # and printing only the required ones
            if ("status" in log and log["status"] == "Pushed") or "aux" in log:
                print(log)
    except docker.errors.APIError as e:
        print(f"Error pushing image to docker hub: {e}")
        raise
    except Exception as e:
        print(f"Error pushing image to docker hub: {e}")
        raise e

    print(f"Successfully pushed {image_full_name} to Docker Hub.")


if __name__ == "__main__":
    # Push the built image to local container registry
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--docker_image",
        type=str,
        required=True,
        help="Full name of the docker image to be pushed.",
    )

    args = parser.parse_args()
    push_image_to_docker_registry(args.docker_image)
