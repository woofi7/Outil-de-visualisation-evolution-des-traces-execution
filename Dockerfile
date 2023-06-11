# Use the base image with CentOS latest
FROM centos:latest

# Set the working directory
WORKDIR /app

# Copy the code into the container
COPY . /app

# Install dependencies
RUN yum update -y && yum install -y python3 python3-pip libX11 libXext libXrender mesa-libGL libxcb git qt5-qtbase-devel gcc gcc-c++ mesa-libGL-devel

# Install pip
RUN yum install -y python3-pip

# Upgrade pip
RUN pip3 install --upgrade pip

# Install requirements
RUN pip install -r requirements.txt

# Set the working directory for running tests
WORKDIR /app/src

# Define the default command to run when the container starts
CMD ["python3", "main.py"]
