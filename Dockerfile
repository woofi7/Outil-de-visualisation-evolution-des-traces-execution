# Use the base image with Python 3.9
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy the code into the container
COPY . /app

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Run tests with coverage
WORKDIR /app/src

# Build the Docker image
RUN docker build -t tommyti/outil-de-visualisation-evolution-des-traces-execution:latest .

# Push the Docker image to a registry
RUN docker push tommyti/outil-de-visualisation-evolution-des-traces-execution:latest
