import boto3
import io
import docx2txt
import PyPDF2
from openpyxl import Workbook
import re
import spacy
from sklearn.metrics.pairwise import cosine_similarity
from tika import parser
from io import BytesIO
from datetime import datetime
import os

# Load the spaCy model for NLP
nlp = spacy.load("en_core_web_lg")

def extract_experience(resume_text):
    pattern = r"(\d+)\s*(?:years?|yrs?)\s*(?:of)?\s*(?:experience)"
    matches = re.findall(pattern, resume_text, re.IGNORECASE)
    if matches:
        return int(matches[0])
    else:
        return 0

def calculate_similarity(text1, text2):
    vector1 = nlp(text1).vector.reshape(1, -1)
    vector2 = nlp(text2).vector.reshape(1, -1)
    similarity_score = cosine_similarity(vector1, vector2)[0][0]
    return similarity_score

def read_doc_with_tika(file_content):
    parsed = parser.from_buffer(file_content)
    return parsed['content']

def search_resumes(bucket_name, search_query, jd):
    matched_resumes = []
    cnt = 0
    s3 = boto3.client('s3')
    
    paginator = s3.get_paginator('list_objects_v2')
    for result in paginator.paginate(Bucket=bucket_name):
        for obj in result.get('Contents', []):
            file_key = obj['Key']
            if file_key.endswith(('.pdf', '.docx', '.txt', '.doc')):
                file_content = s3.get_object(Bucket=bucket_name, Key=file_key)['Body'].read()
                text = ""
                try:
                    if file_key.endswith('.pdf'):
                        pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))
                        num_pages = len(pdf_reader.pages)
                        for page_num in range(num_pages):
                            page = pdf_reader.pages[page_num]
                            text += page.extract_text()
                    elif file_key.endswith('.docx'):
                        text = docx2txt.process(io.BytesIO(file_content))
                    elif file_key.endswith('.doc'):
                        text = read_doc_with_tika(file_content)
                    elif file_key.endswith('.txt'):
                        text = file_content.decode('utf-8', errors='ignore')

                    text = text.lower()
                    input_query = search_query.lower().replace('“', '').replace('”', '').replace('(', '').replace(')', '')
                    input_query_split = input_query.split("and")
                    query_dict = {}
                    for item in input_query_split:
                        query_dict[item] = 0

                    for term in query_dict.keys():
                        if term.__contains__("or"):
                            or_list = term.split("or")
                            for c in or_list:
                                query_dict[term] += text.count(c)
                        else:
                            query_dict[term] += text.count(term)
                    groups_satisfied = all(count > 0 for count in query_dict.values())
                    similarity = calculate_similarity(jd, text)
                    if groups_satisfied:
                        cnt += 1
                        exp = extract_experience(text)
                        similarity = calculate_similarity(jd, text)
                        matched_resumes.append((file_key, "file_path", query_dict, exp, similarity))  # Include exp in the tuple
                except Exception as e:
                    print(f"Error processing {file_key}: {e}")
    return matched_resumes
 
def create_excel(matched_resumes, bucket_name, output_file):
    if matched_resumes:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        output_file_with_timestamp = f"{output_file.split('.')[0]}_{timestamp}.xlsx"
        wb = Workbook()
        ws = wb.active
        ws.append(["Resume", "Path"] + list(matched_resumes[0][2].keys()) + ["Experience"] + ["Score"])

        sorted_resumes = sorted(matched_resumes, key=lambda x: x[4], reverse=True)

        for resume in sorted_resumes:
            ws.append([resume[0], resume[1]] + list(resume[2].values()) + [resume[3]] + [resume[4]])

        output_buffer = BytesIO()
        wb.save(output_buffer)
        output_buffer.seek(0)

        s3 = boto3.client('s3')
        s3.put_object(Bucket=bucket_name, Key=output_file_with_timestamp, Body=output_buffer)

        print("Excel file uploaded successfully to S3:", output_file_with_timestamp)

def lambda_handler(event, context):
    bucket_name = os.getenv('BUCKET_NAME') #'resume-matcher-file'
    search_query = os.getenv('SEARCH_QUERY') #'Oracle and AWS'
    job_description = os.getenv('JOB_DESCRIPTION') #"""Your job description here"""
    output_file = 'matched_resumes.xlsx'
    

    matched_resumes = search_resumes(bucket_name, search_query, job_description)
    create_excel(matched_resumes, bucket_name, output_file)