# Use the base image with Ubuntu latest
FROM ubuntu:latest

# Set the working directory
WORKDIR /app
COPY . /app

# Install dependencies
RUN apt-get update && apt-get upgrade -y && apt-get install -y python3.10 python3-pip libgl1-mesa-glx libxkbcommon-x11-0 libegl1-mesa libglib2.0-0 libdbus-1-3 git qtbase5-private-dev build-essential libgl1-mesa-dev

# Install pip
RUN apt-get install -y python3-pip

# Upgrade pip
RUN pip3 install --upgrade pip

# Install requirements
RUN pip install -r requirements.txt

# Set the working directory for running tests
WORKDIR /app/src

# Define the default command to run when the container starts
# CMD ["python3", "main.py"]
