# Use the base image with CentOS latest
FROM centos:latest

# Set the working directory
WORKDIR /app

# Copy the code into the container
COPY . /app
RUN cd /etc/yum.repos.d/
RUN sed -i 's/mirrorlist/#mirrorlist/g' /etc/yum.repos.d/CentOS-*
RUN sed -i 's|#baseurl=http://mirror.centos.org|baseurl=http://vault.centos.org|g' /etc/yum.repos.d/CentOS-*

# Install pip
RUN yum update -y && \
    yum install -y epel-release python38 python3-pip libX11 libXext libXrender mesa-libGL libxcb git qt5-qtbase-devel gcc gcc-c++ mesa-libGL-devel python3-qt5 libxkbcommon-x11

# Upgrade pip
RUN pip3 install --upgrade pip

RUN pip cache purge
RUN yum install -y epel-release

# Install requirements
RUN pip install -r requirements.txt
RUN pip uninstall opencv-python
RUN pip install opencv-python-headless
# Set the working directory for running tests
WORKDIR /app/src

# Define the default command to run when the container starts
# CMD ["python3", "main.py"]
