import boto3
import time

ec2 = boto3.client('ec2')

# Replace with your instance ID
instance_id = 'i-03bf2b7d5fbfd66db'

# Step 1: Get the availability zone of the instance
response = ec2.describe_instances(InstanceIds=[instance_id])
az = response['Reservations'][0]['Instances'][0]['Placement']['AvailabilityZone']
print(f"Instance AZ: {az}")

# Step 2: Create a new 8GB EBS volume
volume = ec2.create_volume(
    AvailabilityZone=az,
    Size=8,
    VolumeType='gp2',
    TagSpecifications=[{
        'ResourceType': 'volume',
        'Tags': [{'Key': 'Name', 'Value': 'AutomatedEBSVolume'}]
    }]
)
volume_id = volume['VolumeId']
print(f"EBS Volume Created: {volume_id}")

# Step 3: Wait for volume to become available
print("Waiting for volume to become available...")
waiter = ec2.get_waiter('volume_available')
waiter.wait(VolumeIds=[volume_id])
print("Volume is now available.")

# Step 4: Attach the volume to EC2
ec2.attach_volume(
    VolumeId=volume_id,
    InstanceId=instance_id,
    Device='/dev/xvdf'  # typical mount point
)
print(f"Volume {volume_id} attached to {instance_id} at /dev/xvdf")
