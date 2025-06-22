#!/bin/bash

# (Optional) Just a simple restart of docker and your app in case needed

service docker start


# Install dependencies from your cloned repo (adjust path if needed)
sudo -i -u ec2-user pip3 install -r /home/ec2-user/HW1/requirements.txt


python3 --version >> /home/ec2-user/pip_install.log 2>&1 || echo "python3 not found" >> /home/ec2-user/pip_install.log
pip3 --version >> /home/ec2-user/pip_install.log 2>&1 || echo "pip3 not found" >> /home/ec2-user/pip_install.log

# Start backend container if not already running (adjust as needed)
docker run -d -p 8181:8080 igorsakhankov/harbour-cloudcomputing

# Start FastAPI app as ec2-user
sudo -i -u ec2-user nohup python3 /home/ec2-user/HW1/main.py > /home/ec2-user/app.log 2>&1 &
