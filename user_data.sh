#!/bin/bash

# Update OS
yum update -y

# Install docker and python3 (with pip3)
amazon-linux-extras install docker -y
yum install -y python3 python3-pip git

# Start docker service
service docker start

# Wait a moment for docker to be fully up
sleep 5

# Add ec2-user to docker group (effective after next login)
usermod -a -G docker ec2-user

# Check docker and pip3 installed correctly (log output)
docker --version >> /home/ec2-user/docker_run.log 2>&1 || echo "docker not found" >> /home/ec2-user/docker_run.log
python3 --version >> /home/ec2-user/pip_install.log 2>&1 || echo "python3 not found" >> /home/ec2-user/pip_install.log
pip3 --version >> /home/ec2-user/pip_install.log 2>&1 || echo "pip3 not found" >> /home/ec2-user/pip_install.log

# Clone your repo as ec2-user
sudo -i -u ec2-user git clone https://github.com/davitmarg/HW1.git /home/ec2-user/HW1 >> /home/ec2-user/git_clone.log 2>&1

# Upgrade pip as ec2-user
sudo -i -u ec2-user pip3 install --upgrade pip >> /home/ec2-user/pip_upgrade.log 2>&1

# Install Python dependencies as ec2-user
sudo -i -u ec2-user bash -c "cd /home/ec2-user/HW1 && pip3 install -r requirements.txt" >> /home/ec2-user/pip_install.log 2>&1

# Run backend docker container
docker run -d -p 8181:8080 igorsakhankov/harbour-cloudcomputing >> /home/ec2-user/docker_run.log 2>&1

# Wait for backend to start
sleep 10

# Start FastAPI app as ec2-user
sudo -i -u ec2-user nohup python3 /home/ec2-user/HW1/main.py > /home/ec2-user/app.log 2>&1 &
