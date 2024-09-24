# Use the official Python 3.12 image from the Docker Hub
FROM python:3.12-slim

# Install system dependencies
# gcc, libc-dev, musl-dev are needed to compile certain Python packages
# docker.io installs Docker
RUN apt-get update && \
    apt-get install -y --fix-missing build-essential \
    gcc \
    libc-dev \
    musl-dev \
    docker.io \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip to the latest version
RUN pip install --upgrade pip

# Set the working directory in the container
WORKDIR /app

# creating the file to write XComs to
RUN mkdir -p /airflow/xcom
RUN echo "" > /airflow/xcom/return.json

# Configure Poetry to not use virtual environments
ENV POETRY_VIRTUALENVS_CREATE=false

# Copy the pyproject.toml and poetry.lock files
COPY pyproject.toml poetry.lock ./

# Install only non-development dependencies
RUN poetry install --no-dev --no-root

# Copy the rest of the application code into the container
COPY config.yaml .
COPY src ./src

# Add source directory to python path
ENV PYTHONPATH="${PYTHONPATH}:/app/src"

# Set the environment variable
# MLFlow tracking uri
ENV MLFLOW_TRACKING_URI="http://localhost:5000"

# Run the application
CMD ["poetry", "run", "python", "src/main.py"]
