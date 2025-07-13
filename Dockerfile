FROM python:3.10-slim-buster

WORKDIR /app
COPY . /app

# Add these lines
RUN apt-get update && \
    apt-get install -y curl unzip gnupg && \
    rm -rf /var/lib/apt/lists/*

# Then install AWS CLI
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
    unzip awscliv2.zip && \
    ./aws/install && \
    rm -rf awscliv2.zip aws
