FROM amazonlinux:2023

# Install Python 3.11 and other dependencies
RUN dnf install -y python311 zip && \
    dnf clean all && \
    python3.11 -m ensurepip --upgrade && \
    python3.11 -m pip install --upgrade pip virtualenv && \
    python3.11 -m venv base

# Activate the virtual environment
SHELL ["/bin/bash", "-c"]
RUN source base/bin/activate

# Copy requirements file
COPY ./requirements.txt .

# Install dependencies in the virtual environment
RUN pip install -r requirements.txt -t ./python

# Zip it up for deployment
RUN zip -r layer.zip ./python/

# Setting the entrypoint
ENTRYPOINT ["/bin/bash", "-l"]

