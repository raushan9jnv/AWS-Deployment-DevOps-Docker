import boto3
import io
import os
import PyPDF2

def search_resumes(bucket_name, search_query, jd, access_key, secret_key):
    matched_resumes = []
    s3 = boto3.client('s3', aws_access_key_id="AKIA2UC26RDVALSNC56M", aws_secret_access_key="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")

    # List objects in the bucket
    paginator = s3.get_paginator('list_objects_v2')
    for result in paginator.paginate(Bucket=bucket_name):
        for obj in result.get('Contents', []):
            file_key = obj['Key']
            if file_key.endswith(('.pdf', '.docx', '.txt','.doc')):
                print("doc")
                # Download file from S3
                obj = s3.get_object(Bucket=bucket_name, Key=file_key)
                file_content = obj['Body'].read()

                # Read text from different file types
                text = ""
                if file_key.endswith('.pdf'):
                    try:
                        pdf_reader = PyPDF2.PdfFileReader(io.BytesIO(file_content))
                        for page_num in range(pdf_reader.getNumPages()):
                            text += pdf_reader.getPage(page_num).extractText()
                    except PyPDF2._utils.PdfReadError:
                        print("Error reading PDF:", file_key)
                else:
                    text = file_content.decode('utf-8', errors='ignore')

                # Perform search in the text
                if search_query in text:
                    matched_resumes.append(file_key)

    return matched_resumes

# Example usage:
bucket_name = 'resume-matcher-file'
search_query = 'Oracle and AWS'
jd = 'your_job_description'
access_key = 'AKIA2UC26RDVALSNC56M'
secret_key = 'Ehl3heDPxXdP5/F2TX7iDspBOD3PM1eQV2ay5amn'
matched_resumes = search_resumes(bucket_name, search_query, jd, access_key, secret_key)
print("Matched resumes:", matched_resumes)
