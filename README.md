# bridgeAI-model-baseimage

## Model image creation for deployment

1. Set the environment variables given in the below table.
2. Update the python environment in `.env` file
3. Install `poetry` if not already installed
4. Install the dependencies using poetry `poetry install`
5. Add `./src` to the `PYTHONPATH` - `export PYTHONPATH="${PYTHONPATH}:./src"`
6. Run `python src/main.py` or `poetry run python src/main.py`


### Environment Variables

The following environment variables can be set:

| Variable                       | Default Value                      | Description                                                |
|--------------------------------|------------------------------------|------------------------------------------------------------|
| MLFLOW_TRACKING_URI            | `http://localhost:8080`            | The URI for the MLflow tracking server                     |
| DEPLOY_MODEL_NAME              | `house_price_prediction_prod`      | The name of the model to be deployed                       |
| DEPLOY_MODEL_ALIAS             | `champion`                         | The alias for the deployed model                           |
| DOCKER_REGISTRY                | `localhost:5000`                   | The Docker registry where images are stored                |
| MLFLOW_BUILT_IMAGE_NAME        | `mlflow_model`                     | The name of the MLflow model Docker image                  |
| MLFLOW_BUILT_IMAGE_TAG         | `latest`                           | The tag for the MLflow model Docker image                  |
| MODEL_DOCKER_BUILD_CONTEXT_PVC | `model_docker_build_context_pvc`   | Name of the PVC allocated for this DAG                     |
| MODEL_DOCKER_PUSH_SECRET       | `ecr-credentials`                  | Name of the secret to authenticate ECR access              | 



### Running the tests

Ensure that you have the project requirements already set up by following the [Model image creation for deployment](#model-image-creation-for-deployment) instructions
- Ensure `pytest` is installed. `poetry install` will install it as a dev dependency.
- - For integration tests, set up the dependencies (MLFlow) by running, `docker-compose up -d`
- Run the tests with `poetry run pytest ./tests`