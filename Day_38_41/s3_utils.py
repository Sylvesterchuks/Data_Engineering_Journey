from utils import * #s3_resource, s3_client, pd, io, upload_to_s3, download_from_s3

def list_created_buckets(S3_BUCKET_PREFIX):
    response = s3_client.list_buckets()
    print("Listing Amazon S3 Buckets:")
    for bucket in response['Buckets']:
        if S3_BUCKET_PREFIX in bucket['Name']:
            print(f"-- {bucket['Name']}")


def get_working_bucket(S3_BUCKET_PREFIX):
    working_buckets = []
    for mybucket in s3_resource.buckets.all():
        if S3_BUCKET_PREFIX in mybucket.name:
            working_buckets.append(mybucket)
    return working_buckets



def upload_retrieve_data(S3_BUCKET_NAME, data_to_upload, folder_prefix='', format='json', dtype=False):
    # data_to_upload = {df_name : df} #, 'Roadway_Block.geojson':road_block_df_json}

    upload_to_s3(S3_BUCKET_NAME, data_to_upload, folder_prefix=folder_prefix, format=format, dtype=dtype)
    my_dict = download_from_s3(S3_BUCKET_NAME, folder_prefix, format=format)
    return my_dict
