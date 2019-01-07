import boto3
import requests
from requests_aws4auth import AWS4Auth

host = 'https://vpc-cloud-dev-1234567890.us-east-1.es.amazonaws.com/' # include https:// and trailing /
region = 'us-east-1' 
service = 'es'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

# Register repository

path = '_snapshot/<s3-bucket-name>' 
url = host + path

payload = {
  "type": "s3",
  "settings": {
    "bucket": "<s3-bucket-name>",
    "region": "us-west-2",
    "role_arn": "arn:aws:iam::1234567890:role/ElasticSearchSnapshotRole"
  }
}

headers = {"Content-Type": "application/json"}

r = requests.put(url, auth=awsauth, json=payload, headers=headers)

print(r.status_code)
print(r.text)
