# Use the base image with Python 3.9
FROM python:3.9-windowsservercore

# Set the working directory
WORKDIR /app

# Copy the code into the container
COPY . /app

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Set the working directory for running tests
WORKDIR /app/src

# Update the WORKDIR directive above if necessary

# Define the default command to run when the container starts
CMD ["python", "main.py"]
