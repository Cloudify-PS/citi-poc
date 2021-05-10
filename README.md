## _Blueprints prepared for PoC for CITI._
This repository contains blueprints for generating two types of environments:
- A deployment of `setup-rds.yaml` blueprint creates all necessary network resources on AWS (VPCs, Subnets, IPs, NICs, Security Groups, Internet Gateways, DNS), Load Balancer and generates certificates used by Wordpress application it installs. AWS RDS is used as a main database.
- A deployment of `setup-mariadb.yaml` blueprint creates all necessary network resources on AWS (VPCs, Subnets, IPs, NICs, Security Groups, Internet Gateways, DNS), Load Balancer and generates certificates used by Wordpress application it installs. An external database - MariaDB - is used as a main database.
## Prerequisites
### ROSA installation
_ROSA == Red Hat Openshift Service on AWS_  
To start running these setups, the user has to have two separate OpenShift clusters installed.  
A possible way of doing it, is to use ROSA (Red Hat Openshift Service on AWS). It's a tool, which automates the whole process of installing Openshift on top of the AWS infrastructure. In the end, you get a fully operational OpenShift cluster, with its own AWS VPC & all relevant resources defined.  
In order to use it, user has to have at least a minimal set of permissions in its AWS account defined here: https://docs.openshift.com/rosa/rosa_getting_started/rosa-aws-prereqs.html#rosa-minimum-spc_prerequisites
### Installing OpenShift clusters using ROSA
All the steps to install the cluster are described in official ROSA documentation: https://docs.openshift.com/rosa/rosa_getting_started/rosa-creating-cluster.html.  
You should provide Node CIDR, Service CIDR and Pod CIDR as described in the documentation.
### NGINX ingress controller
One of the goals of this poc was to configure SSL termination on the OpenShift side, instead of configuring it on AWS load balancer. To make that possible, we decided to use `ingress` service. Following the k8s documentation, `ingress` is "an API object that manages external access to the services in a cluster, typically HTTP. Ingress may provide load balancing, SSL termination and name-based virtual hosting."  
To make that work, we needed an ingress controller to enable that function. We chose NGINX ingress controller, which was installed using the `Operators -> OperatorHub` page, which can be accessed in OpenShift dashboard.  
When ingress controller is installed, it creates a dedicated load balancer in a VPC, where cluster is running. When `ingress` object is being created, it maps the K8s service to a NodePort, to which the load balancer can send the traffic. There is also the subdomain defined in the `ingress` object. To make it work, a DNS record (alias) has to be set in the domain, to route the traffic coming on that address to the load balancer.
### Permanent cluster-admin token
After the cluster is installed, there are several additional steps in the configuration.  
Create a service account as it is described there: https://docs.openshift.com/container-platform/3.5/rest_api/index.html and save the token as our new password.
Additionally, the new service account needs to have a cluster-role binding with the cluster-admin user created.  
For example:
1. `oc create serviceaccount cloudify`
2. `oc policy add-role-to-user cluster-admin system:serviceaccount:default:cloudify`
3. `oc policy add-role-to-user cluster-admin cluster-role:serviceaccount:default:cloudify`
4. `oc serviceaccounts get-token cloudify`
### Ingress controller
Go to my-ingress-controller-service in OpenShift console and change its type to LoadBalancer by adding an annotation. This enforces Load Balancer's configuration to become a network load balancer.  
In the my-ingress-controller-service YAML code find `annotation` section and add:  
```yaml
service.beta.kubernetes.io/aws-load-balancer-type: nlb
```
### EFS
There needs to be one EFS per VPC - the reason is that the provided hostname for EFS service is not visible outside the VPC. The name is `<file system id>.efs.<region>.amazonaws.com`. Alternative would be to create one with DNS name and use only that one (but this was not tested).  
To create EFS:
1. Go to EFS service in AWS console and choose File Systems
2. Click on Create File System
3. Click on customize and provide all needed data  
 All can be left as default by some optons can be changed for POC:
    - availability: Regional
    - deselect: "Enable automatic backups"
    - deselect: "Enable encryption of data at rest"
#### Create Security Groups
Create security groups in VPC that will allow all traffic in (alternative - you can limit it to cluster IPs and NFS port).  
You will have to create a SG for each VPC in use.
#### Assign Security Groups
1. Go to file system definition in EFS and click on the ID
2. Go to network tab
3. Assign SG to the EFS filesystem ID
#### Create Storage Class
Create a Storage Class in OpenShift following the documentation: https://docs.openshift.com/container-platform/4.6/storage/persistent_storage/persistent-storage-efs.html
## Manager
Create a manager in AWS and configure it or restore from snapshot.  
Snapshot location https://drive.google.com/file/d/1rjdA9aAuZQazoem1jWGcoVL81BwnjoKu/view?usp=sharing
After restoring from snapshot review the secrets and update all that have `CHANGEME` value.
### Plugins
To run these blueprints, you have to upload the following plugins to your Cloudify Manager instance running in chosen AWS region.
Instructions on how to use them in your own application are linked below.
| Plugin | URL |
| ------ | ------ |
| cloudify-aws-plugin | [cloudify-aws-plugin](https://github.com/cloudify-cosmo/cloudify-aws-plugin/releases) |
| cloudify-terraform-plugin | [cloudify-terraform-plugin](https://github.com/cloudify-cosmo/cloudify-terraform-plugin/releases) |
| cloudify-kubernetes-plugin | [cloudify-kubernetes-plugin](https://github.com/cloudify-cosmo/cloudify-ansible-plugin/releases) |
| cloudify-utilities-plugin | [cloudify-utilities-plugin](https://github.com/cloudify-cosmo/cloudify-kubernetes-plugin/releases) |
| cloudify-ansible-plugin | [cloudify-ansible-plugin](https://github.com/cloudify-incubator/cloudify-utilities-plugin/releases) |
### Secrets
BLueprints require following secrets to be created in the Cloudify Manager:
- `aws_access_key` - AWS key ID to connect to AWS account
- `aws_secret_key` - AWS Secret key to connect to AWS account
- `db_password` - password to be set for the database
- `db_username` - name of the user to be set for the database
- `github_password` - token generated in your GitHub account to access Terraform files
- `github_username` - your GitHub username to access Terraform files
- `hosted_zone_id` - ID of the hosted zone to create DNS records in
- `openshift_namespace` - OpenShift namespace, default: `default`
### Tenants
For the purpose of the POC for CITI we created two tenants:
- `PROD` with blueprints to deploy setup with RDS as a main database
- `COB` with blueprints to deploy setup with MariaDB as a main database
## RDS-based Wordpress application running on two redundant OpenShift clusters
In order to deploy a full setup of RDS-based Wordpress application running on two redundant OpenShift clusters follow above instructions and install two separate OpenShift clusters.  
Upload blueprint from https://github.com/Cloudify-PS/citi-poc/archive/refs/heads/rds.zip to your Cloudify Manager - as a main blueprint file specify `setup-rds.yaml`.  
Provide all necessary inputs - in most cases the default value would be fine.
The `setup-rds.yaml` blueprint uses namespace mechanism to import and execute blueprints for each module:
- `certificate` - creates a new VM with all necessary networking resources, generates certificates on that VM and stores them in runtime properties and creates a kubernetes secrets with newly created certificates as values
- `backend-rds` - creates and configures an AWS RDS instance for a particular cluster, sets up VPC peering for communication
- `application` - installs Wordpress application on desired OpenShift Kubernetes cluster. Creates Persistent Volume, Persistent Volume Claim, Wordpress Service and Wordpress Deployment
- `load-balancer` - instantiates and configures an AWS Network Load Balancer, connects it to the workers nodes from both clusters and creates a final DNS record for the specified domain
## MariaDB-based Wordpress application running on two redundant OpenShift clusters
WIP - not fully tested yet  
A second option is to deploy the whole setup using MariaDB as a main database - instead of AWS RDS. The setup would consist of the additional VM with an external database installed and running on it.  
All other parts and resources of the deployment stay the same, the only difference is the database used by Wordpress application running on Openshift clusters.  


In order to deploy a full setup of MariaDB-based Wordpress application running on two redundant OpenShift clusters follow above instructions and install two separate OpenShift clusters.  
Upload blueprint from https://github.com/Cloudify-PS/citi-poc/archive/refs/heads/main.zip to your Cloudify Manager - as a main blueprint file specify `setup-mariadb.yaml`.  
Provide all necessary inputs - in most cases the default value would be fine.
The `setup-mariadb.yaml` blueprint uses namespace mechanism to import and execute blueprints for each module:
- `certificate` - creates a new VM with all necessary networking resources, generates certificates on that VM and stores them in runtime properties and creates a kubernetes secrets with newly created certificates as values
- `backend-mariadb` - creates a new VM with all necessary networking resources and installs MariaDB service on it using `Ansible` plugin, provides comprehensive configuration of the database itself as well as the networking and connectivity between the database and workers from OpenShift clusters
- `application` - installs Wordpress application on desired OpenShift Kubernetes cluster. Creates Persistent Volume, Persistent Volume Claim, Wordpress Service and Wordpress Deployment
- `load-balancer` - instantiates and configures an AWS Network Load Balancer, connects it to the workers nodes from both clusters and creates a final DNS record for the specified domain
