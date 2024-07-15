import boto3
s3 = boto3.client('s3', aws_access_key_id="AKIA2UC26RDVALSNC56M", aws_secret_access_key="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")
bucket_name = 'resume-matcher-file'

    # List objects in the bucket
paginator = s3.get_paginator('list_objects_v2')
for result in paginator.paginate(Bucket=bucket_name):
    #  print(result)
     for obj in result.get('Contents', []):
        file_key = obj['Key']
        if file_key.endswith(('.pdf', '.docx', '.txt','.doc')):
        
            # Download file from S3
            obj = s3.get_object(Bucket=bucket_name, Key=file_key)
            file_content = obj['Body']
            print(file_content)