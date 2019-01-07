import boto3
import requests
from requests_aws4auth import AWS4Auth

host = 'https://search-robotstats-1234567890.us-west-1.es.amazonaws.com/' # include https:// and trailing /
region = 'us-west-1' 
service = 'es'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)


# Take snapshot

path = '_snapshot/<s3-bucket-name>/snap-1'
url = host + path

r = requests.put(url, auth=awsauth)

print(r.text)
