#!/bin/bash

# Define your image name
IMAGE_NAME="stockquote_image"

# Go to your script directory
cd "your directory"

# Create a Dockerfile if it doesn't exist
if [ ! -f Dockerfile ]; then
cat > Dockerfile <<EOF
# Use an official Python runtime as a parent image
FROM python:3.10.7

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run script_worker.py when the container launches
CMD ["python3", "script_worker.py"]
EOF
fi

# Build the Docker image
docker build -t $IMAGE_NAME .

