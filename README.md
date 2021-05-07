# citi-poc

## Setup

# Manager
Create a  manager in AWS and configure it or restore from snapshot
Snapshot https://drive.google.com/file/d/1qkxyC_iQtwkF7e4W-FeZmTE4mqy8W9KG/view?usp=sharing


## Create EFS
There needs to be one EFS per VPC - the reason is that the provided hostname for EFS service is not visible outside the VPC. The name is <file system id>.efs.<region>.amazonaws.com
Alternative would be to create one with DNS name and use only one (but this was not tested)

To create EFS go to EFS service and choose File Systems
Click on Create File System
Click on customize and provide all needed data
 All can be left as default by some optons can be changed for POC:
  - Availibility: Regional
  - deselect "Enable automatic backups"
  - deselect: "Enable encryption of data at rest"

Create Security Groups
Create security groups in VPC that will allow all traffic in (Alternative you can limit it to cluster IPs and NFS port)
You will have to create a SG for each VPC in use

Assign SGs
Go to file system definition in EFS and cluck on the ID
Go to network tab
Assign SG to the EFS filesystem id

# Blueprints 

Blueprints prepared for PoC for CITI. 

- A deployment of `setup-rds.yaml` blueprint creates all necessary network resources on AWS (VPCs, Subnets, IPs, NICs, Security Groups, Internet Gateways, DNS), Load Balancer and generates certificates used by Wordpress application it installs. AWS RDS is used as a main database.
- A deployment of `setup-mariadb.yaml` blueprint creates all necessary network resources on AWS (VPCs, Subnets, IPs, NICs, Security Groups, Internet Gateways, DNS), Load Balancer and generates certificates used by Wordpress application it installs. An external database - MariaDB - is used as a main database.
