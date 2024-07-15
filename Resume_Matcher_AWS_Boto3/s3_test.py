import boto3
s3 = boto3.resource(
    service_name = 's3',
    region_name ='ap-southeast-2',
    aws_access_key_id = "AKIA2UC26RDVALSNC56M",
    aws_secret_access_key="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"
)

# for bucket in s3.buckets.all():
#     print(bucket.name)

import os
import boto3

# Assuming you have configured your AWS credentials using AWS CLI or environment variables

s3_client = boto3.client('s3')

# Replace 'bucket_name' with your actual S3 bucket name
# bucket_name = 'resume-matcher-file'

import boto3
import os
import PyPDF2
import docx2txt
from tika import parser

def retrieve_files_from_s3(bucket_name):
    files = []
    s3 = boto3.client('s3')
    paginator = s3.get_paginator('list_objects_v2')
    result = paginator.paginate(Bucket=bucket_name)

    for page in result:
        if "Contents" in page:
            for key in page["Contents"]:
                file_name = key["Key"]
                if file_name.endswith(('.pdf', '.docx', '.txt', '.doc')):
                    files.append(file_name)

    return files

# Usage
bucket_name = 'resume-matcher-file'
files = retrieve_files_from_s3(bucket_name)
print(files)
