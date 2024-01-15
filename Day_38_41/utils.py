
# interact with aws
import boto3

# system manipulation
import os
import io
import pathlib
from glob import glob
import uuid
from getpass import getpass


# to handle certificate verification
import certifi

# to manage json data
import json
# import geopandas as gpd

# for pandas dataframes
import pandas as pd

# datetime, argparse
import time
import datetime
from math import ceil
import argparse

# a simple logging message
import logging

# using request library
import requests

import opendatasets as od



# custom modules
# from config import *
from aws_credential import *


# AWS S3 Services

def create_bucket_name(bucket_prefix):
    return ''.join([bucket_prefix, str(uuid.uuid4())])

def create_bucket(S3_BUCKET_PREFIX, s3):
    session = boto3.session.Session()
    AWS_REGION = session.region_name
    
    S3_BUCKET_NAME = create_bucket_name(S3_BUCKET_PREFIX)
    if AWS_REGION == 'us-east-1':
        response = s3.create_bucket(Bucket=S3_BUCKET_NAME)
    else:
        location = {'LocationConstraint': AWS_REGION}
        response = s3.create_bucket(Bucket=S3_BUCKET_NAME,
                                    CreateBucketConfiguration=location)
    print(f"Amazon S3 {S3_BUCKET_NAME} bucket has been created in {AWS_REGION}")
    return S3_BUCKET_NAME, response
 

def bucket_exists_cli(bucketName):
    response = s3_client.list_buckets()
    for bucket in response['Buckets']:
        if bucketName == bucket['Name']:
            return True
    return False

def bucket_exists_res(bucket):
    return s3_resource.Bucket(bucket) in s3_resource.buckets.all()


def upload_path(local_directory, bucket, destination, certain_upload=False):

  # enumerate local files recursively
    for root, dirs, files in os.walk(local_directory):

        for filename in files:

            # construct the full local path
            local_path = os.path.join(root, filename)

            # construct the full Dropbox path
            relative_path = os.path.relpath(local_path, local_directory)
            s3_path = os.path.join(destination, relative_path)

            if certain_upload:
                s3_client.upload_file(local_path, bucket, s3_path)
                return

            print('Searching "%s" in "%s"' % (s3_path, bucket))
            try:
                s3_client.head_object(Bucket=bucket, Key=s3_path)
                # print("Path found on S3! Skipping %s..." % s3_path)
            except:
                print("Uploading %s..." % s3_path)
                s3_client.upload_file(local_path, bucket, s3_path)


def enable_version(bucket_name):
    versioning = s3_resource.BucketVersioning(bucket_name)
    versioning.enable()
    print(f'S3 Bucket versioning: {versioning.status}')

    
    
# Transformation functions
    
def get_time(x):
    if x >= 5 and x < 12:
        return 'morning'
    elif x >= 12 and x < 17:
        return 'afternoon'
    elif x >= 17 and x < 21:
        return 'evening'
    else:
        return 'night'
    
    
def flat_items(d, key_separator='.'):
    """
    Flattens the dictionary containing other dictionaries like here: https://stackoverflow.com/questions/6027558/flatten-nested-python-dictionaries-compressing-keys

    >>> example = {'a': 1, 'c': {'a': 2, 'b': {'x': 5, 'y' : 10}}, 'd': [1, 2, 3]}
    >>> flat = dict(flat_items(example, key_separator='_'))
    >>> assert flat['c_b_y'] == 10
    """
    for k, v in d.items():
        if type(v) is dict:
            for k1, v1 in flat_items(v, key_separator=key_separator):
                yield key_separator.join((k, k1)), v1
        else:
            yield k, v
            
            
def json_stream(value, S3_BUCKET_NAME, FileName, has_date=True):
    json_buffer = io.StringIO()

    if has_date:
        # Create dataframe and convert to pandas
        value.to_json(json_buffer, orient='records', date_format = 'iso', date_unit='s')
    else:
        # Create dataframe and convert to pandas
        value.to_json(json_buffer, orient='index', index=True)

    response = s3_client.put_object(Body=json_buffer.getvalue(),
                                    Bucket=S3_BUCKET_NAME,
                                    Key=FileName)
    
    
def csv_stream(value, S3_BUCKET_NAME, FileName):
    csv_buffer = io.StringIO()

    # Create dataframe and convert to pandas
    value.to_csv(csv_buffer, index=False)

    response=s3_client.put_object(Body=csv_buffer.getvalue(),
                                Bucket=S3_BUCKET_NAME,
                                Key=FileName)


def upload_to_s3(S3_BUCKET_NAME, data_to_upload, folder_prefix, format='csv', dtype=False):
    for key, value in data_to_upload.items():
        FileName = f'{folder_prefix}_{datetime.datetime.now().date()}/{key}'
        if format=='csv':
            csv_stream(value, S3_BUCKET_NAME, FileName)
        elif format=='json':
            json_stream(value, S3_BUCKET_NAME, FileName)
        if dtype:
            dtt = pd.DataFrame([dict(zip(value.dtypes.keys(),[str(col).replace('|','') for col in value.dtypes.values]))]).T
            json_stream(dtt, S3_BUCKET_NAME, f"{FileName.split('.')[0]}Datatype.json", has_date=False)

def download_from_s3(S3_BUCKET_NAME, folder_prefix, format='csv'):
    my_dict = {}

    for key in s3_client.list_objects(Bucket=S3_BUCKET_NAME, Prefix=folder_prefix)['Contents']:
        print(key['Key'])

        df_name = key['Key'].split('/')[-1].split('.')[0].split('-')[0]

        obj = s3_client.get_object(Bucket= S3_BUCKET_NAME ,
                                   Key = key['Key'])

        if key['Key'].split('.')[-1] == 'csv':
            my_dict[df_name]  = pd.read_csv(io.BytesIO(obj['Body'].read()), parse_dates=True, infer_datetime_format=True, encoding='utf8')
        elif key['Key'].split('.')[-1] == 'json':
            my_dict[df_name]  = pd.read_json(io.BytesIO(obj['Body'].read()), orient='records', encoding='utf8')
    return my_dict
