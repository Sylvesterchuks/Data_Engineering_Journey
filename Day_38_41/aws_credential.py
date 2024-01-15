import os
import boto3
from dotenv import load_dotenv


load_dotenv()

AWS_DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION") # 'us-east-2' # change to your own region
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID") # getpass('Enter AWS Access Key ID: ') #'*********AHZ4IVO******'
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY") # getpass('Enter AWS Secret Access Key: ') #'****4W4*******QW1W*****************'

AWS_REGION = boto3.session.Session().region_name

s3_client = boto3.client("s3", region_name=AWS_REGION, verify=False)

s3_resource = boto3.resource(
    service_name='s3',
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    verify=False
)
