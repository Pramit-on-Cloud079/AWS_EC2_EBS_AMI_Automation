import boto3
import time

ec2 = boto3.client('ec2')

# === UPDATE THESE ===
instance_id = 'i-03bf2b7d5fbfd66db'
volume_id = 'vol-062a9b554dd979614'
ami_id = 'ami-0957e542bd9109cf7'

# Check if volume is attached before detaching
volume = ec2.describe_volumes(VolumeIds=[volume_id])['Volumes'][0]
attachments = volume.get('Attachments', [])

if attachments:
    print("Detaching EBS volume...")
    ec2.detach_volume(VolumeId=volume_id, InstanceId=instance_id, Device='/dev/xvdf')
    
    # Wait until volume is detached
    print("Waiting for volume to detach...")
    while True:
        vol = ec2.describe_volumes(VolumeIds=[volume_id])['Volumes'][0]
        state = vol['Attachments'][0]['State'] if vol['Attachments'] else 'detached'
        if state == 'detached':
            print("Volume detached.")
            break
        print("Still detaching...waiting 5 seconds.")
        time.sleep(5)
else:
    print("Volume already detached.")

# Step 1: Detach EBS volume
# print("Detaching EBS volume...")
# ec2.detach_volume(VolumeId=volume_id, InstanceId=instance_id, Device='/dev/xvdf')

# Wait until volume is detached
# print("Waiting for volume to detach...")
# while True:
    #vol = ec2.describe_volumes(VolumeIds=[volume_id])['Volumes'][0]
    #state = vol['Attachments'][0]['State'] if vol['Attachments'] else 'detached'
    #if state == 'detached':
        #print("Volume detached.")
        #break
    #print("Still detaching...waiting 5 seconds.")
    #time.sleep(5)

# Step 2: Delete volume
print("Deleting EBS volume...")
ec2.delete_volume(VolumeId=volume_id)
print("Volume deleted.")

# Step 3: Get snapshot ID linked to AMI
print("Fetching AMI snapshot ID...")
image = ec2.describe_images(ImageIds=[ami_id])['Images'][0]
snapshot_id = image['BlockDeviceMappings'][0]['Ebs']['SnapshotId']
print(f"Snapshot ID: {snapshot_id}")

# Deregister AMI
print("Deregistering AMI...")
ec2.deregister_image(ImageId=ami_id)

# Wait for a few seconds (safe delay)
time.sleep(5)

# Fetch associated snapshot ID
print("Fetching AMI snapshot ID...")
images = ec2.describe_images(ImageIds=[ami_id])['Images']
if images:
    snapshot_id = images[0]['BlockDeviceMappings'][0]['Ebs']['SnapshotId']

    # Delete snapshot
    print("Deleting snapshot...")
    ec2.delete_snapshot(SnapshotId=snapshot_id)
else:
    print("AMI not found or snapshot already deleted.")

# Optional: Terminate EC2 (uncomment if you want)
print("Terminating EC2...")
ec2.terminate_instances(InstanceIds=[instance_id])
print("EC2 termination initiated.")
