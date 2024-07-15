import boto3
import os
import PyPDF2
# import docx
import docx2txt
from tika import parser

# Initialize Boto3 S3 client
s3 = boto3.client('s3', aws_access_key_id="AKIA2UC26RDVALSNC56M", aws_secret_access_key="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")

# Define function to process PDF files
def process_pdf(file_obj):
    pdf_reader = PyPDF2.PdfReader(file_obj['Body'])
    for page in pdf_reader.pages:
        text = page.extract_text()
        print("pdf",text)
        # Do something with the text

# Define function to process DOCX files
def process_docx(file_obj):
    text = docx2txt.process(file_obj['Body'])
    # Do something with the text
    print("docx2txt",text)

# Define function to process DOC files
def process_doc(file_obj):
    raw = parser.from_file(file_obj['Body'])
    text = raw['content']
    # Do something with the text
    print("text",text)

# Define function to process TXT files
def process_txt(file_obj):
    text = file_obj['Body'].read().decode('utf-8')
    # Do something with the text
    print("docx2txt",text)

# Iterate through files in S3 bucket
def process_s3_bucket(bucket_name):
    paginator = s3.get_paginator('list_objects_v2')
    for page in paginator.paginate(Bucket=bucket_name):
        for obj in page['Contents']:
            key = obj['Key']
            extension = os.path.splitext(key)[1].lower()

            # Get file from S3
            file_obj = s3.get_object(Bucket=bucket_name, Key=key)

            # Apply processing based on file extension
            if extension == '.pdf':
                process_pdf(file_obj)
            elif extension == '.docx':
                process_docx(file_obj)
            elif extension == '.doc':
                process_doc(file_obj)
            elif extension == '.txt':
                process_txt(file_obj)
            else:
                print(f"Ignoring file with unsupported extension: {key}")

# Replace 'your-bucket-name' with your actual S3 bucket name
process_s3_bucket('resume-matcher-file')
