import boto3
from datetime import datetime

ec2 = boto3.client('ec2')

# Replace with your EC2 instance ID
instance_id = 'i-03bf2b7d5fbfd66db'

# Step 1: Generate unique name with timestamp
timestamp = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
ami_name = f'custom-ami-from-script-{timestamp}'

# Step 2: Create AMI from the EC2 instance
response = ec2.create_image(
    InstanceId=instance_id,
    Name=ami_name,
    NoReboot=True,  # Prevents EC2 from restarting
    TagSpecifications=[
        {
            'ResourceType': 'image',
            'Tags': [{'Key': 'Name', 'Value': ami_name}]
        }
    ]
)

ami_id = response['ImageId']
print(f"Custom AMI creation started: {ami_id}")
print(f"Name: {ami_name}")

# Step 3: Wait for AMI to become available
print("Waiting for AMI to become available...")
waiter = ec2.get_waiter('image_available')
waiter.wait(ImageIds=[ami_id])
print(f"✅ AMI {ami_id} is now available and ready to use.")
