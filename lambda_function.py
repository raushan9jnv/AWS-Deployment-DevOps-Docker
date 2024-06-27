import json
import boto3
import textract
import re
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

s3 = boto3.client('s3')


# Function to clean text (you can expand this as needed)
def clean_text(text):
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with a single space
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation and special characters
    return text.strip()  # Strip leading/trailing whitespace


# Function to extract text from various document formats
def extract_text_from_s3_object(bucket, key):
    try:
        file_content = s3.get_object(Bucket=bucket, Key=key)['Body'].read()

        # Determine file type and extract text accordingly
        if key.endswith('.pdf'):
            text = textract.process(file_content, encoding='utf-8')
        elif key.endswith(('.doc', '.docx')):
            text = textract.process(file_content)
        elif key.endswith('.txt'):
            text = file_content.decode('utf-8')
        else:
            return ""  # Unsupported file format

        return clean_text(text.decode('utf-8'))

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
    bucket = event['bucket']
    job_description = event['job_description']
    skills = event['skills']

    try:
        response = s3.list_objects_v2(Bucket=bucket)
        resumes = []
        keys = []

        if 'Contents' in response:
            for item in response['Contents']:
                key = item['Key']
                text = extract_text_from_s3_object(bucket, key)
                if text:
                    resumes.append(text)
                    keys.append(key)

        similarities = compare_resumes(job_description, skills, resumes)
        best_match_index = similarities.argmax()
        best_match_key = keys[best_match_index]

        return {
            'statusCode': 200,
            'best_match_key': best_match_key,
            'similarity_score': similarities[best_match_index]
        }

    except (NoCredentialsError, PartialCredentialsError):
        return {
            'statusCode': 403,
            'message': 'Credentials are not available'
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'message': str(e)
        }
