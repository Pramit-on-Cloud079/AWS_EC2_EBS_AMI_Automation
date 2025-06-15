import boto3
import time

ec2 = boto3.client('ec2')

# === UPDATE THESE ===
instance_id = 'i-xxxxxxxxxxxxxxxxx'
volume_id = 'vol-xxxxxxxxxxxxxxxxx'
ami_id = 'ami-xxxxxxxxxxxxxxxxx'
manual_snapshot_ids = ['snap-xxxxxxxxxxxxxxxxx']  # Add more if needed

# Step 1: Detach EBS volume (if attached)
print("Checking volume attachment...")
volume = ec2.describe_volumes(VolumeIds=[volume_id])['Volumes'][0]
attachments = volume.get('Attachments', [])

if attachments:
    print("Detaching EBS volume...")
    ec2.detach_volume(VolumeId=volume_id, InstanceId=instance_id, Device='/dev/xvdf')
    print("Waiting for volume to detach...")
    while True:
        vol = ec2.describe_volumes(VolumeIds=[volume_id])['Volumes'][0]
        state = vol['Attachments'][0]['State'] if vol['Attachments'] else 'detached'
        if state == 'detached':
            print("✅ Volume detached.")
            break
        print("Still detaching...waiting 5 seconds.")
        time.sleep(5)
else:
    print("Volume already detached.")

# Step 2: Delete EBS volume
print("Deleting EBS volume...")
ec2.delete_volume(VolumeId=volume_id)
print("✅ Volume deleted.")

# Step 3: Get snapshot ID from AMI (before deregistering)
print("Getting AMI snapshot ID...")
image = ec2.describe_images(ImageIds=[ami_id])['Images'][0]
snapshot_id = image['BlockDeviceMappings'][0]['Ebs']['SnapshotId']
print(f"Snapshot ID: {snapshot_id}")

# Step 4: Deregister AMI
print("Deregistering AMI...")
ec2.deregister_image(ImageId=ami_id)
print("✅ AMI deregistered.")

# Step 5: Delete snapshot linked to AMI
print("Waiting 5 seconds before deleting snapshot...")
time.sleep(5)
print(f"Deleting snapshot {snapshot_id}...")
ec2.delete_snapshot(SnapshotId=snapshot_id)
print("✅ AMI snapshot deleted.")

# Step 6: Delete manually created snapshots
for snap_id in manual_snapshot_ids:
    try:
        print(f"Deleting manual snapshot {snap_id}...")
        ec2.delete_snapshot(SnapshotId=snap_id)
        print(f"✅ Snapshot {snap_id} deleted.")
    except Exception as e:
        print(f"Error deleting snapshot {snap_id}: {e}")

# Step 7: Terminate EC2 instance
print(f"Terminating EC2 instance {instance_id}...")
ec2.terminate_instances(InstanceIds=[instance_id])
print("✅ EC2 termination initiated.")
