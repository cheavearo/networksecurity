FROM python:3.10-slim-buster
WORKDIR /app
COPY . /app

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y curl unzip && \
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
    unzip awscliv2.zip && \
    ./aws/install && \
    rm -rf awscliv2.zip aws


RUN apt-get update && pip install -r requirements.txt
CMD ["python3", "app.py"]
