import boto3
from botocore.exceptions import NoCredentialsError
import botocore
from pyunpack import Archive
import os
import shutil

def upload_to_aws(local_file, s3_file):
    bucket = "il-s3--portabilityauto-du"
    s3 = boto3.client('s3',)
    print('uploading')
    try:
        s3.upload_file(local_file, bucket, s3_file)
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False

def image_presigned_url(file_name):
    bucket_name = 'il-s3--portabilityauto-du'
    location = 'ap-south-1'
    #location = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
    #                        aws_secret_access_key=SECRET_KEY).get_bucket_location(Bucket=bucket_name)[
    #    'LocationConstraint']
    s3_client = boto3.client(
        's3',
        region_name=location,
    )
    url = s3_client.generate_presigned_url(
        ClientMethod='get_object',
        Params={'Bucket': bucket_name, 'Key': file_name, },
        ExpiresIn=600000,
    )
    return url

def image_sas_url(claim_number):
    combined_url = []
    s3 = boto3.client('s3',)
    bucket_name = "il-s3--portabilityauto-du"
    resp = s3.list_objects_v2(Bucket=bucket_name)
    # print(resp)
    print("claim in sas",claim_number)
    for i in range(len(resp.get('Contents'))):

        key = resp.get('Contents')[i].get('Key')
        # print(key)
        if str(key).__contains__(claim_number) and str(key).replace('/',"") != claim_number:
            # print(key)
            #location = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
             #            aws_secret_access_key=SECRET_KEY).get_bucket_location(Bucket=bucket_name)['LocationConstraint']
            location = 'ap-south-1'
            s3_client = boto3.client(
                's3',
                region_name=location,
            )
            url = s3_client.generate_presigned_url(
                ClientMethod='get_object',
                Params={'Bucket': bucket_name, 'Key': key, },
                ExpiresIn=600000,
            )
            combined_url.append(url)
    # print("combined",combined_url)
    return combined_url

