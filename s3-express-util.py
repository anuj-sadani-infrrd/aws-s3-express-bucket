import os
import time
import logging
import boto3
from botocore.exceptions import ClientError, NoCredentialsError

# Your AWS credentials
aws_access_key_id = "my-key"
aws_secret_access_key = "my-secret"
region = "us-west-2"


def list_buckets(s3_client):
    response = s3_client.list_buckets()

    for bucket in response["Buckets"]:
        print(bucket["Name"])


def list_directory_buckets(s3_client):
    response = s3_client.list_buckets()

    for bucket in response["Buckets"]:
        print(bucket["Name"])


def create_express_bucket(s3_client, bucket_name, availability_zone):
    """
    [Note] IAM user must have s3express:CreateBucket role
    [Refer] https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-express-security-iam.html
    """
    try:
        bucket_config = {
            "Location": {"Type": "AvailabilityZone", "Name": availability_zone},
            "Bucket": {"Type": "Directory", "DataRedundancy": "SingleAvailabilityZone"},
        }
        s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=bucket_config)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def download_from_s3(s3_client, s3_bucket_name, s3_directory_path, local_directory):
    """
    [Note] This download from both General and Express S3
    Make sure it has access to both s3 and s3express policies
    """
    st = time.time()

    # List objects in the S3 directory
    s3_objects = s3_client.list_objects_v2(Bucket=s3_bucket_name, Prefix=s3_directory_path)

    # Download each object from S3 to the local directory
    for s3_object in s3_objects.get("Contents", []):
        s3_key = s3_object["Key"]
        local_file_path = os.path.join(local_directory, os.path.basename(s3_key))

        # Create the local directory if it doesn't exist
        os.makedirs(os.path.dirname(local_file_path), exist_ok=True)

        # Download the file from S3
        s3_client.download_file(s3_bucket_name, s3_key, local_file_path)
        print(f"Downloaded: {s3_key}")

    print(f"Download completed in {time.time()-st}")


def upload_to_s3(s3_client, local_directory, bucket, s3_prefix):
    st = time.time()
    for root, dirs, files in os.walk(local_directory):
        for filename in files:
            # Generate the S3 key by joining the s3_prefix and the relative path to the file
            s3_key = os.path.join(s3_prefix, os.path.relpath(os.path.join(root, filename), local_directory))
            try:
                s3_client.upload_file(os.path.join(root, filename), bucket, s3_key)
                print(f"Successfully uploaded {s3_key}")
            except NoCredentialsError:
                print("AWS credentials not available.")
                return
    print(f"Uploaded to S3, took {time.time() -st} secs")


# Create the S3 client using your AWS credentials
s3_client = boto3.client(
    "s3", region_name=region, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key
)

"""
List General purpose S3 bucket
"""
list_buckets(s3_client)

"""
List Express S3 bucket
[Note] You must have the s3express:ListAllMyDirectoryBuckets permission in an IAM identity-based policy
[Refer] https://docs.aws.amazon.com/AmazonS3/latest/API/API_ListDirectoryBuckets.html
"""
list_directory_buckets(s3_client)


"""
Create the S3 express bucket
[Note] The express bucket name should be in a given format
[Refer] https://docs.aws.amazon.com/AmazonS3/latest/userguide/directory-bucket-naming-rules.html
"""
bucket_name = "dev01-infrrd-express-ml--usw2-az1--x-s3"
availability_zone = "usw2-az1"
create_express_bucket(s3_client, bucket_name, availability_zone)

"""
Download the model from S3
"""
download_from_s3(
    s3_client=s3_client, s3_bucket_name="sagemaker-dev01-ml", s3_directory_path="illm-v7", local_directory="illm-v7"
)


# Upload the directory to S3
# The prefix (folder) in S3 where you want to upload the contents
upload_to_s3(
    s3_client=s3_client,
    local_directory="illm-v7",
    bucket="dev01-infrrd-express-ml--usw2-az1--x-s3",
    s3_prefix="illm-v7",
)
