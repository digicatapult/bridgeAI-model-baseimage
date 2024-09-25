"""Main entry point."""

import os

from src.build_mlflow_docker_image import (build_from_dockerfile,
                                           generate_docker_file,
                                           modify_dockerfile)
from src.get_mlflow_model_details import get_model_run_uri
from src.push_image_to_cr import push_image_to_dockerhub
from src.utils import set_mlflow_tracking_uri

if __name__ == "__main__":
    mlflow_tracking_uri = os.getenv(
        "MLFLOW_TRACKING_URI", "http://mlflow-tracking:80"
    )
    model_name = os.getenv("DEPLOY_MODEL_NAME", "house_price_prediction_prod")
    model_alias = os.getenv("DEPLOY_MODEL_ALIAS", "champion")
    model_docker_image_name = os.getenv(
        "MODEL_DOCKER_IMAGE", "house_price_model"
    )
    mlflow_build_base_image = os.getenv(
        "MODEL_DOCKER_IMAGE", "python:3.12-slim"
    )

    image_name = "mlflow_model"
    image_tag = "latest"

    set_mlflow_tracking_uri(mlflow_tracking_uri)

    model_uri = get_model_run_uri(mlflow_tracking_uri, model_name, model_alias)

    generate_docker_file(model_uri)

    modify_dockerfile()
    build_from_dockerfile(image_name=image_name, image_tag=image_tag)

    # Optional at the moment
    push_image_to_dockerhub(image_name, image_tag, use_cli=True)

    """
    # Now manually load the generated image
    to local kind cluster using the following command from cli
        $ kind load docker-image mlflow_model:\
            latest --name bridgeai-gitops-infra
    
    # Then ensure the kserve-inference.yaml 
    is modified to deploy form docker image
    ```yaml
    apiVersion: "serving.kserve.io/v1beta1"
    kind: "InferenceService"
    metadata:
      name: "house-price"
      annotations:
          serving.kserve.io/deploymentMode: RawDeployment
          serving.kserve.io/gateway-disableIngressCreation: "true"
          serving.kserve.io/gateway-disableIstioVirtualHost: "true"
    spec:
      predictor:
        minReplicas: 1
        maxReplicas: 1
        containers:
          - name: "mlflow-regression-model"
            image: "mlflow_model:latest"
            ports:
              - containerPort: 8080
                protocol: TCP
            env:
              - name: PROTOCOL
                value: "v2"
            resources:
              requests:
                memory: "4Gi"
                cpu: "2"
              limits:
                memory: "5Gi"  # Increase memory limit to avoid OOMKilled
                cpu: "3"
    ```
    Note: without `minReplicas: 1` and `maxReplicas: 1` 
    the pod is restarting because of some error;
    
    ```
    Warning   FailedGetResourceMetric        
    HorizontalPodAutoscaler/house-price-predictor                    
    failed to get cpu utilization: unable to get metrics for resource cpu: 
    unable to fetch metrics from resource metrics API: 
    the server could not find the requested resource (get pods.metrics.k8s.io)
    ```
    
    Now run
        $ kubectl apply -f kserve-inference.yaml
        
        
    $ kubectl get inferenceservice house-price 
    NAME          URL                                      READY   
    PREV   LATEST   PREVROLLEDOUTREVISION   LATESTREADYREVISION
       AGE
    house-price   http://house-price-default.example.com   True                                                                  
    41m

    """
