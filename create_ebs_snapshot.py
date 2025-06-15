import boto3
from datetime import datetime

ec2 = boto3.client('ec2')

# Replace with your EC2 instance ID
instance_id = 'i-03bf2b7d5fbfd66db'

# Step 1: Get the root volume ID
volumes = ec2.describe_instances(InstanceIds=[instance_id])
root_volume_id = volumes['Reservations'][0]['Instances'][0]['BlockDeviceMappings'][0]['Ebs']['VolumeId']

# Step 2: Create a snapshot with timestamp
timestamp = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
description = f'Snapshot of {root_volume_id} taken on {timestamp}'

snapshot = ec2.create_snapshot(
    VolumeId=root_volume_id,
    Description=description,
    TagSpecifications=[{
        'ResourceType': 'snapshot',
        'Tags': [{'Key': 'Name', 'Value': f'snapshot-{timestamp}'}]
    }]
)

print(f"✅ Snapshot started: {snapshot['SnapshotId']}")
