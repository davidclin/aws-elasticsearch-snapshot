# aws-elasticsearch-snapshot
David's Cheatsheet on how to take Elasticsearch Snapshot


Example Python Script to Pre-sign and Register Bucket
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

# Register repository

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
