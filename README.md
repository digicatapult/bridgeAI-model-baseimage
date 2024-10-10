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

| Variable                    | Default Value                   | Description                                                                                                                                          |
|-----------------------------|---------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------|
| MLFLOW_TRACKING_URI         | `https://mlflow.dc-mlops.co.uk` | The URI for the MLFlow tracking server. Use `http://mlflow-tracking:80` for kind cluster                                                             |
| MLFLOW_TRACKING_USERNAME    | None                            | MLFlow tracking username. In kind cluster no need to set it as there is no authentication needed, but ensure that you set it on Production cluster.  | 
| MLFLOW_TRACKING_PASSWORD    | None                            | MLFlow tracking password. In kind cluster no need to set it as there is no authentication needed, but ensure that you set it on Production cluster.  | 
| DEPLOY_MODEL_NAME           | `house_price_prediction_prod`   | The name of the model to be deployed                                                                                                                 |
| DEPLOY_MODEL_ALIAS          | `champion`                      | The alias for the deployed model                                                                                                                     |



### Running the tests

Ensure that you have the project requirements already set up by following the [Model image creation for deployment](#model-image-creation-for-deployment) instructions
- Ensure `pytest` is installed. `poetry install` will install it as a dev dependency.
- - For integration tests, set up the dependencies (MLFlow) by running, `docker-compose up -d`
- Run the tests with `poetry run pytest ./tests`