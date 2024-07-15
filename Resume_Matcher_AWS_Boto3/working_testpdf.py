import boto3
import io
from PyPDF2 import PdfReader


s3 = boto3.client('s3', aws_access_key_id="AKIA2UC26RDVALSNC56M", aws_secret_access_key="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")
def list_objects(bucket_name):
    paginator = s3.get_paginator('list_objects_v2')
    for page in paginator.paginate(Bucket=bucket_name):
        for obj in page.get('Contents', []):
            yield obj['Key']

def process_pdf(bucket_name, file_key):
    obj = s3.get_object(Bucket=bucket_name, Key=file_key)
    if file_key.endswith('.pdf'):
        pdf_file = obj['Body'].read()
        pdf_reader = PdfReader(io.BytesIO(pdf_file))
        num_pages = len(pdf_reader.pages)
        text = ''
        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
        return text
    else:
        return None
def process_bucket(bucket_name):
    for file_key in list_objects(bucket_name):
        text = process_pdf(bucket_name, file_key)
        if text:
            print(f"Text extracted from {file_key}:")
            print(text)
bucket_name = 'resume-matcher-file'
process_bucket(bucket_name)
