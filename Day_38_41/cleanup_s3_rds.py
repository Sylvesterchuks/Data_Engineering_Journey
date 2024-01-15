from utils import *
from s3_utils import *
from get_data import retrieve_data

S3_BUCKET_PREFIX = "service-call-dc-"

BASE_DIR = os.getcwd() #pathlib.Path(__file__).parent.resolve()


### Deleting RDS MySQL using Boto3 resource
def cleanup_rds():
    client = boto3.client('rds', AWS_REGION, verify=False)
    response = client.describe_db_instances()

    for instance in response["DBInstances"]:
        print ("About to delete %s" %(instance['DBInstanceIdentifier']))
        if input('Enter Y/N to continue: ').lower()=='y':
            if instance['DeletionProtection']:
                response = client.modify_db_instance(
                                                        DBInstanceIdentifier=instance['DBInstanceIdentifier'],
                                                        DeletionProtection=False
                                                    )
            response = client.delete_db_instance(DBInstanceIdentifier=instance['DBInstanceIdentifier'],
                                                SkipFinalSnapshot=True,
                                                DeleteAutomatedBackups=True
            )
            print(f"{instance['DBInstanceIdentifier']} successfully deleted!!!")
    


def clean_up_s3():
    # s3_resource = boto3.resource("s3", region_name=AWS_REGION)
    buckets = [bucket for bucket in s3_resource.buckets.all() if S3_BUCKET_PREFIX in bucket.name]
    print(buckets)

    def cleanup_s3_bucket(s3_bucket):
        # Deleting objects
        for s3_object in s3_bucket.objects.all():
            s3_object.delete()
        # Deleting objects versions if S3 versioning enabled
        for s3_object_ver in s3_bucket.object_versions.all():
            s3_object_ver.delete()
        print(f"{mybucket.name} S3 Bucket cleaned up")

    for mybucket in buckets:
        s3_bucket = s3_resource.Bucket(mybucket.name)
    
        cleanup_s3_bucket(s3_bucket)
        s3_bucket.delete()
        print(f"{mybucket.name} S3 Bucket deleted")

if __name__=="__main__":
    clean_up_s3()
    cleanup_rds()