#!/usr/env/bin python

import random
import string

from cloudify import ctx
from cloudify.state import ctx_parameters
from cloudify.exceptions import NonRecoverableError

CLUSTER_A = 'os-cb-cluster1'
CLUSTER_B = 'os-cb-cluster2'

API = 'api_config'
NETWORK = 'network_config'

RUNTIME_PROPERTY = 'openshift_cluster'

configuration = {
    RUNTIME_PROPERTY: {}
}

cluster_name = ctx_parameters['cluster_name']

if cluster_name == CLUSTER_A:
    configuration[RUNTIME_PROPERTY][API] = {
        "host": "https://api.os-cb-cluster1.w1b2.p1.openshiftapps.com:6443",
        "api_key": "eyJhbGciOiJSUzI1NiIsImtpZCI6IjVJM0l1M0poMzBuMWx4bDVlR2toSF9qbURCTWxDczN3ZnZGdWRXX2o0eHcifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJkZWZhdWx0Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZWNyZXQubmFtZSI6ImV4YW1wbGVzLXVzZXItdG9rZW4tNzdtcWwiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoiZXhhbXBsZXMtdXNlciIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6Ijg3MGVjNGY3LWI5MTMtNDMxNy05Y2M2LTU3YjBiOTRlYWUyOCIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDpkZWZhdWx0OmV4YW1wbGVzLXVzZXIifQ.N_403uAz-1Uhc_1KEAPrN1ewwSV8W3rFHfG9VF2jR1icutOeDBeRZjVXZxhphrtnn8EXuNsih93tGggeeti-euJMayCwKWOt5Rsbuk5u1hggsF5hrF7SlUQw4b8TCs1zkYKe8NfAjIMpcW6rtkg7LVw3n7jGdfj21zESoLjo32lGY64k3_3ObakEyxmH_blZET86iMo_TmNteUXulAkIBuxb3WecZrxI4cRl6eazvD4oXoqdqKPgeeMh48eHHqDHlvz-AGV-07UbzPvKYMbRqNlX36W7NnZugpV56wP9uR_98cx3Sv7bCc8lvCEfai9g7aSXo7ruinZI0x3ZFOSC0Q",
        "debug": false,
        "verify_ssl": false
    }
    configuration[RUNTIME_PROPERTY][NETWORK] = {
        "cluster_name": "os-cb-cluster1",
        "vpc": "vpc-01f23fec9019e8f4c",
        "public_subnet": "subnet-003311ac114cc7dba",
        "route_tb": "rtb-0c5ee5b09eda70143",
        "security_group": "sg-090d730343326f2cf",
        "instances": [
            "i-099b43bec984ab7e5",
            "i-0463df568c1aa7e66",
            "i-0d62c1d224156e85d",
            "i-09f1d2de035025d02",
            "i-021811b728f181fc5",
            "i-09a56aaf3f1e4ff13",
            "i-0018d3b701eeeb140"
        ]
    }
elif cluster_name == CLUSTER_B:
    configuration[RUNTIME_PROPERTY][API] = {
        "host": "https://api.os-cb-cluster2.ccif.p1.openshiftapps.com:6443",
        "api_key": "sha256~0ZYTp7WTf6Ot44Rrj7zZh1GtWwlUGbWBZO5rYbPUOUg",
        "debug": false,
        "verify_ssl": false
    }
    configuration[RUNTIME_PROPERTY][NETWORK] = {
        "cluster_name": "os-cb-cluster2",
        "vpc": "vpc-0ec3c7bcafea43a99",
        "public_subnet": "subnet-013004ef27a8bd393",
        "route_tb": "rtb-088df2c51e2082310",
        "security_group": "sg-0fc8ddf0d72e610e8",
        "instances": [
            "i-041fe1bc3ac69fa80",
            "i-0cf10177163a4529f",
            "i-0a874e009daf126af",
            "i-03d854125d6b7fd65",
            "i-0e79cc215ccac1239",
            "i-0a53aef8171a6e301",
            "i-0dbc9810689968bb4"
        ]
    }
else:
    raise Exception("Unhandled cluster name: {}".format(cluster_name))

ctx.instance.runtime_properties.update(configuration)