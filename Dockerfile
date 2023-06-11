# Use the base image with CentOS latest
FROM centos:latest

# Set the working directory
WORKDIR /app

# Copy the code into the container
COPY . /app
RUN cd /etc/yum.repos.d/
RUN sed -i 's/mirrorlist/#mirrorlist/g' /etc/yum.repos.d/CentOS-*
RUN sed -i 's|#baseurl=http://mirror.centos.org|baseurl=http://vault.centos.org|g' /etc/yum.repos.d/CentOS-*
# Install dependencies
RUN yum update -y && yum install -y python3

# Install requirements
RUN pip install -r requirements.txt

# Set the working directory for running tests
WORKDIR /app/src

# Define the default command to run when the container starts
CMD ["python3", "main.py"]
