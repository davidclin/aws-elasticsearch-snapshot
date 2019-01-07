import boto3
import requests
from requests_aws4auth import AWS4Auth

host = 'https://search-test-1234567890.es.amazonaws.com/' # include https:// and trailing /
region = 'us-west-2' # e.g. us-west-1
service = 'es'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

# Restore snapshots (all indices)

path = '_snapshot/<s3-bucket-name>/snap-1/_restore'
url = host + path

r = requests.post(url, auth=awsauth)

print(r.text)
