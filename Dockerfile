# Use the base image with Python 3.9
FROM python:3.8

# Set the working directory
WORKDIR /app

# Copy the code into the container
COPY . /app

# Install dependencies
RUN apt-get update && apt install libgl1-mesa-glx -y && apt-get install -y python3-opencv && pip install opencv-python && pip install opencv-python-headless && pip install opencv-contrib-python && pip install opencv-contrib-python-headless==4.5.3.56
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Set the working directory for running tests
WORKDIR /app/src

# Update the WORKDIR directive above if necessary

# Define the default command to run when the container starts
CMD ["python", "main.py"]
