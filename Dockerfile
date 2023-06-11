# Use the base image with Python 3.9
FROM ubuntu:latest

# Set the working directory
WORKDIR /app

# Copy the code into the container
COPY . /app

# Install dependencie
RUN apt update
RUN apt install python3.10-venv -y
RUN python3.10 -m venv venv
RUN . venv/bin/activate
RUN apt install python3.10 -y
# RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Set the working directory for running tests
WORKDIR /app/src

# Update the WORKDIR directive above if necessary

# Define the default command to run when the container starts
CMD ["python", "main.py"]
