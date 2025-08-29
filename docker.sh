#!/bin/bash

# TO RUN
# Build the Docker image
docker build -t site .
# Run the Docker container
docker run -p 8080:8080 site