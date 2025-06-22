import boto3

client = boto3.client('ec2')

instance_id = 'i-09692be5d272ge9f9'  

response = client.create_image(
    InstanceId=instance_id,
    Name='HW2-Custom',
    NoReboot=False
)

image_id = response['ImageId']
print("AMI ID:", image_id)
