from python:3.14

arg USER=user

env DEBIAN_FRONTEND=noninteractive

run apt update && apt upgrade -y && \
    apt install -y git build-essential sudo && \
    apt update && \
    apt upgrade && \
    apt clean

run useradd -m -s /bin/bash $USER && \
    mkdir -p /etc/sudoers.d/ && \
    echo "$USER ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers.d/$USER && \
    chmod 0440 /etc/sudoers.d/$USER

user $USER

workdir /app

copy requirements.txt .
run pip install -r requirements.txt

copy . .
