# aws-elasticsearch-snapshot
David's Cheatsheet on how to take Elasticsearch Snapshot

Resource: [Working with Amazon Elasticsearch Service Index Snapshots](https://docs.aws.amazon.com/elasticsearch-service/latest/developerguide/es-managedomains-snapshots.html#es-managedomains-snapshot-create)

## Steps
1) Send a signed request to register the snapshot directory
2) Take snapshot of Elasticsearch domain
3) Restore (Optional)

## Requirements
1) The host where Python script and curl command(s) get invoked must have IP connectivity to the ES endpoint.
   If the host is an EC2 instance on a private subnet, you will need to route requests through a NAT gateway and permit the NAT gateway's public IP in the ES domain's access policy.
   If the host is an EC2 instance with a public IP address, you will need to permit the public IP address of the instance in the ES domain's access policy. 
   If the host is behind a VPN firewall, you will need to permit the public IP address of the firewall in the ES domain's access policy.
   
2) Role must have S3 permissions among other 

## Example Python Script to Sign Requests and Register Bucket
<pre>
import boto3
import requests
from requests_aws4auth import AWS4Auth

host = 'https://search-inventoryservice-ni7kkw2izko47dar34epivxgo4.us-west-2.es.amazonaws.com/' # include https:// and trailing
/
region = 'us-west-2' # e.g. us-west-1
service = 'es'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

## Register repository

path = '_snapshot/tars-elasticsearch-snapshots-us-west-2' # the Elasticsearch API endpoint
url = host + path

payload = {
  "type": "s3",
  "settings": {
    "bucket": "tars-elasticsearch-snapshots-us-west-2",
    "region": "us-west-2",
    "role_arn": "arn:aws:iam::accountid:role/ElasticSearchSnapshotRole"  <----  replace accountid with actual account ID
  }
}

headers = {"Content-Type": "application/json"}

r = requests.put(url, auth=awsauth, json=payload, headers=headers)

print(r.status_code)
print(r.text)

# # Take snapshot
#
# path = '_snapshot/my-snapshot-repo/my-snapshot'
# url = host + path
#
# r = requests.put(url, auth=awsauth)
#
# print(r.text)
#
# # Delete index
#
# path = 'my-index'
# url = host + path
#
# r = requests.delete(url, auth=awsauth)
#
# print(r.text)
#
# # Restore snapshots (all indices)
#
# path = '_snapshot/my-snapshot-repo/my-snapshot/_restore'
# url = host + path
#
# r = requests.post(url, auth=awsauth)
#
# print(r.text)
#
# # Restore snapshot (one index)
#
# path = '_snapshot/my-snapshot-repo/my-snapshot/_restore'
# url = host + path
#
# payload = {"indices": "my-index"}
#
# headers = {"Content-Type": "application/json"}
#
# r = requests.post(url, auth=awsauth, json=payload, headers=headers)
#
# print(r.text)

</pre>


## Role requirements
Trust relationship for es.amazonaws.com service

<pre>
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "",
      "Effect": "Allow",
      "Principal": {
        "Service": "es.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
</pre>

## Take snapshot

<pre>
TBD
</pre>

## Work in Progress
===========================
To manually take a snapshot

   0) document existing ES domain parameters including access policy
   1) register repository using register-repo.py
   2) curl -XPUT 'elasticsearch-domain-endpoint/_snapshot/repository/snapshot-name'

===========================
To see all snapshot repositories

   curl -XGET 'elasticsearch-domain-endpoint/_snapshot?pretty'

===========================
To verify the state of all snapshots of your domain

   curl -XGET 'elasticsearch-domain-endpoint/_snapshot/repository/_all?pretty'


===========================
To restore all snapshots to a new domain

   0) Create new domain with similar ES domain parameters including access policy
      where the access-policy uses the name of the new domain instead of the old.
      
      Don't blindly copy/paste an access policy from one ES domain to the new one.

   1) Register repository with new domain using register-repo-with-new-domain.py

   2) Use the restore-snapshot.py script to restore ES domain.
    
   3) If you get error 'cannot restore index [.kibana] because it's open' follow
      instructions here:

      https://aws.amazon.com/premiumsupport/knowledge-center/elasticsearch-kibana-error/
