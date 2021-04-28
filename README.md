# citi-poc

Blueprints prepared for PoC for Citi. 

- A deployment of `setup-rds.yaml` blueprint creates all necessary network resources on AWS (VPCs, Subnets, IPs, NICs, Security Groups, Internet Gateways, DNS), Load Balancer and generates certificates used by Wordpress application it installs. AWS RDS is used as a main database.
- A deployment of `setup-mariadb.yaml` blueprint creates all necessary network resources on AWS (VPCs, Subnets, IPs, NICs, Security Groups, Internet Gateways, DNS), Load Balancer and generates certificates used by Wordpress application it installs. An external database - MariaDB - is used as a main database.
