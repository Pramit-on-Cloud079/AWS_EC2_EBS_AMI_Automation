# 🚀 EC2 + EBS + AMI Automation using Boto3 (AWS Python SDK)

This project demonstrates full automation of key AWS EC2 operations using Python and Boto3:

- Attaching a new EBS volume on an existing EC2
- Creating a custom AMI
- Cleaning up all associated resources (Instance, Volume, AMI, Snapshot, EC2)

---

## 📁 Project Structure

aws-ec2-ebs-ami-automation/
├── create_ebs_VOLUME.py # Launch EC2 and attach EBS
├── create_custom_ami.py # Create AMI from EC2 instance
├── clean_up_resources.py # Delete volume, Deregister AMI, delete snapshot and terminate instance
├── README.md # Project documentation

---

## ⚙️ Technologies Used

- Python 3.11+
- Boto3 (AWS SDK for Python)
- AWS EC2
- AWS EBS
- AWS AMI

---

## 🔐 Prerequisites

- AWS CLI configured with IAM credentials
- Python installed on local machine
- Boto3 installed (`pip install boto3`)
- Key pair and security group created in AWS

---

## 📌 Steps Performed

1. Launch EC2 with automation
2. Attach additional EBS volume
3. Create a custom AMI
4. Clean up all AWS resources via script
5. Deregister AMI and delete its snapshot

---

## 🧹 Cleanup Reminder

⚠️ Always terminate unused EC2 instances and delete volumes, AMIs, and snapshots to avoid charges.

---

## 🖼️ Project Screenshots

📸 Screenshots of EBS volume, AMI, and web server setup have been added for documentation and portfolio showcasing.

---

## 📇 Author

**Pramit Dasgupta**  
AWS Certified Solutions Architect Associate  
AWS Certified AI Practitioner  

---

## 📢 License

This project is for learning and demonstration purposes. Free to reuse with credit.