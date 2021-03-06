import random
import logging
import boto3
import os
from botocore.exceptions import ClientError

def create_presigned_url(bucket_name, object_name, expiration=3600):
    """Generate a presigned URL to share an S3 object

    :param bucket_name: string
    :param object_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """

    # Generate a presigned URL for the S3 object
    s3_client = boto3.client(
      's3',
      aws_access_key_id=os.environ['AWS_KEY'],
      aws_secret_access_key=os.environ['AWS_SECRET']
    )
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL
    return response

def list_files(bucket):
    """
    Function to list files in a given S3 bucket
    """
    s3 = boto3.client('s3')
    contents = []

    try:
        for item in s3.list_objects_v2(Bucket=bucket)['Contents']:
            contents.append(item)
    except Exception as e:
        pass

    return contents

def get_random_image(bucket):
    files = list_files(bucket)

    if files:
        random_index = random.randrange(0, len(files))
        return files[random_index]

    return None
    