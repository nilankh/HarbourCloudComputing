import boto3
import time
import requests

ec2 = boto3.resource('ec2')
client = boto3.client('ec2')

# 🕒 Start measuring time
start_time = time.time()

# Launch instance
instances = ec2.create_instances(
    ImageId='ami-0b8d8a07002d54801',
    MinCount=1,
    MaxCount=1,
    InstanceType='t2.nano',
    KeyName='hwkey',
    SecurityGroupIds=['sg-0537bb99dc63f63da'],
    UserData=open('new_script.sh').read(),
    TagSpecifications=[{
        'ResourceType': 'instance',
        'Tags': [{'Key': 'Name', 'Value': 'HW2-From-Snapshot'}]
    }]
)
instance = instances[0]
instance_id = instance.id

print(f"Waiting for instance {instance_id} to be in 'running' state...")
instance.wait_until_running()
instance.load()  # Refresh to get public IP

# 🕒 Option A: Time when instance is running
running_time = time.time()
print(f"[INFO] Instance running in {running_time - start_time:.2f} seconds")

# Wait until HTTP response (i.e., app is ready)
url = f"http://{instance.public_dns_name}:5000"
print(f"Waiting for app to be ready at {url}...")

timeout = 300
while True:
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            break
    except Exception:
        pass
    if time.time() - running_time > timeout:
        print("App failed to start within 5 mins")
        break
    time.sleep(5)

# 🕒 Option B: Time when app is ready
ready_time = time.time()
print(f"[INFO] App ready in {ready_time - start_time:.2f} seconds")
