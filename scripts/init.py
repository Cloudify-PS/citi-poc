#!/usr/env/bin python

import random
import string

from cloudify import ctx
from cloudify.state import ctx_parameters
from cloudify.exceptions import NonRecoverableError

CLUSTER_A = 'os-cb-cluster1'
CLUSTER_B = 'os-cb-cluster3'

API = 'api_config'
NETWORK = 'network_config'
EFS = 'efs_config'

configuration = {}

cluster_name = ctx_parameters['cluster_name']

if cluster_name == CLUSTER_A:
    configuration[API] = {
        "host": "https://api.os-cb-cluster1.w1b2.p1.openshiftapps.com:6443",
        "api_key": "eyJhbGciOiJSUzI1NiIsImtpZCI6IjVJM0l1M0poMzBuMWx4bDVlR2toSF9qbURCTWxDczN3ZnZGdWRXX2o0eHcifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJkZWZhdWx0Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZWNyZXQubmFtZSI6ImV4YW1wbGVzLXVzZXItdG9rZW4tNzdtcWwiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoiZXhhbXBsZXMtdXNlciIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6Ijg3MGVjNGY3LWI5MTMtNDMxNy05Y2M2LTU3YjBiOTRlYWUyOCIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDpkZWZhdWx0OmV4YW1wbGVzLXVzZXIifQ.N_403uAz-1Uhc_1KEAPrN1ewwSV8W3rFHfG9VF2jR1icutOeDBeRZjVXZxhphrtnn8EXuNsih93tGggeeti-euJMayCwKWOt5Rsbuk5u1hggsF5hrF7SlUQw4b8TCs1zkYKe8NfAjIMpcW6rtkg7LVw3n7jGdfj21zESoLjo32lGY64k3_3ObakEyxmH_blZET86iMo_TmNteUXulAkIBuxb3WecZrxI4cRl6eazvD4oXoqdqKPgeeMh48eHHqDHlvz-AGV-07UbzPvKYMbRqNlX36W7NnZugpV56wP9uR_98cx3Sv7bCc8lvCEfai9g7aSXo7ruinZI0x3ZFOSC0Q",
        "debug": False,
        "verify_ssl": False
    }
    configuration[NETWORK] = {
        "cluster_name": "os-cb-cluster1",
        "vpc": {
            "id": "vpc-01f23fec9019e8f4c",
            "cidr": "10.0.0.0/16"
        },
        "public_subnet": "subnet-003311ac114cc7dba",
        "route_tb": "rtb-0c5ee5b09eda70143",
        "security_group": "sg-090d730343326f2cf",
        "instances": [
            # "i-099b43bec984ab7e5",
            # "i-0463df568c1aa7e66",
            # "i-0d62c1d224156e85d",
            "i-09f1d2de035025d02",
            "i-021811b728f181fc5",
            # "i-09a56aaf3f1e4ff13",
            # "i-0018d3b701eeeb140"
        ]
    }
    configuration[EFS] = {
        "url": "fs-6d72ae36.efs.eu-central-1.amazonaws.com"
    }
elif cluster_name == CLUSTER_B:
    configuration[API] = {
        "host": "https://api.os-cb-cluster3.p3w0.p1.openshiftapps.com:6443",
        "api_key": "sha256~nCyR9AfQLuu7G2byW6O4Qw1ksgeUVRFSkGjKam_g5HM",
        "debug": False,
        "verify_ssl": False
    }
    configuration[NETWORK] = {
        "cluster_name": "os-cb-cluster3",
        "vpc": {
            "id": "vpc-0d43b67165d8735a0",
            "cidr": "10.100.0.0/16"
        },
        "public_subnet": "subnet-09a7ea444dcd8d6df",
        "route_tb": "rtb-092da85f1bb7f83ab",
        "security_group": "sg-03aec47c6205f5771",
        "instances": [
            "i-0472a8990fe102cb4",
            "i-0462d2b9234956219"
        ]
    }
    configuration[EFS] = {
        "url": "fs-1272ae49.efs.eu-central-1.amazonaws.com"
    }
else:
    raise Exception("Unhandled cluster name: {}".format(cluster_name))

ctx.instance.runtime_properties.update(configuration)