import json
import boto3
import re
import os
import io
import PyPDF2
import docx2txt
import textract
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
import string

s3 = boto3.client('s3')

def clean_text(text):
    text = re.sub(r'\s+', ' ', text).strip()
    text = text.replace("\xa0", " ")
    text = re.sub(r'\s+([' + re.escape(string.punctuation) + r'])', r'\1', text)
    text = re.sub(r'[^\x20-\x7E]', '', text)
    return text

def extract_text_from_s3_object(bucket, key):
    try:
        obj = s3.get_object(Bucket=bucket, Key=key)
        file_content = obj['Body'].read()

        text = ""
        if key.lower().endswith('.pdf'):
            pdf_file = io.BytesIO(file_content)
            reader = PyPDF2.PdfReader(pdf_file)
            for page_num in range(len(reader.pages)):
                text += reader.pages[page_num].extract_text()
        elif key.lower().endswith('.docx'):
            temp_file_path = '/tmp/tempfile.docx'
            with open(temp_file_path, 'wb') as temp_file:
                temp_file.write(file_content)
            text = docx2txt.process(temp_file_path)
            os.remove(temp_file_path)
        elif key.lower().endswith('.doc'):
            temp_file_path = '/tmp/tempfile.doc'
            with open(temp_file_path, 'wb') as temp_file:
                temp_file.write(file_content)
            text = textract.process(temp_file_path).decode('utf-8', errors='ignore')
            os.remove(temp_file_path)
        elif key.lower().endswith('.txt'):
            text = file_content.decode('utf-8')

        if not text:
            text = textract.process(io.BytesIO(file_content)).decode('utf-8', errors='ignore')

        return clean_text(text)

    except Exception as e:
        print(f"Error extracting text from {key}: {e}")
        return ""

def compare_resumes(job_description, skills, resumes):
    documents = [job_description + " " + skills] + resumes
    vectorizer = TfidfVectorizer().fit_transform(documents)
    vectors = vectorizer.toarray()
    cosine_similarities = cosine_similarity(vectors[0:1], vectors[1:]).flatten()
    return cosine_similarities

def lambda_handler(event, context):
    # print(f"Received event: {json.dumps(event)}")

    # Check if 'body' exists in the event and parse it if it does
    if 'body' in event:
        body = json.loads(event['body'])
    else:
        body = event

    # print(f"Parsed body: {json.dumps(body)}")

    # Extract parameters from the body
    bucket = body.get('bucket')
    job_description = body.get('job_description')
    skills = body.get('skills')

    missing_params = []
    if not bucket:
        missing_params.append('bucket')
    if not job_description:
        missing_params.append('job_description')
    if not skills:
        missing_params.append('skills')

    if missing_params:
        message = {'message': f"Missing parameters: {', '.join(missing_params)}"}
        return {
            'statusCode': 400,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps(message)
        }

    try:
        response = s3.list_objects_v2(Bucket=bucket)
        resumes = []
        keys = []

        if 'Contents' in response:
            for item in response['Contents']:
                key = item['Key']
                if not key.lower().endswith(('.pdf', '.doc', '.docx', '.txt', '.rtf')):
                    continue
                text = extract_text_from_s3_object(bucket, key)
                if text:
                    resumes.append(text)
                    keys.append(key)

        if not resumes:
            message = {'message': 'No resumes could be processed.', 'processed_resumes_count': len(resumes)}
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps(message)
            }

        similarities = compare_resumes(job_description, skills, resumes)
        best_match_index = similarities.argmax()
        best_match_key = keys[best_match_index]

        message = {
            'message': 'Execution started successfully!',
            'best_match_key': best_match_key,
            'similarity_score': similarities[best_match_index],
            'processed_resumes_count': len(resumes)
        }

        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps(message)
        }

    except (NoCredentialsError, PartialCredentialsError):
        message = {'message': 'Credentials are not available'}
        return {
            'statusCode': 403,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps(message)
        }
    except Exception as e:
        print(f"Exception occurred: {e}")
        message = {'message': str(e)}
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps(message)
        }
