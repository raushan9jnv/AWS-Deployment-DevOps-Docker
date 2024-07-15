import boto3
import io
import os
import docx2txt
import PyPDF2
from openpyxl import Workbook
import re
import spacy
from sklearn.metrics.pairwise import cosine_similarity
from tika import parser

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

def read_doc_with_tika(file_path):
    parsed = parser.from_file(file_path)
    return parsed['content']

def search_resumes(bucket_name, search_query, jd, access_key, secret_key):
    matched_resumes = []
    s3 = boto3.client('s3', aws_access_key_id="AKIA2UC26RDVALSNC56M", aws_secret_access_key="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")

    paginator = s3.get_paginator('list_objects_v2')
    for result in paginator.paginate(Bucket=bucket_name):
        for obj in result.get('Contents', []):
            file_key = obj['Key']
            if file_key.endswith(('.pdf', '.docx', '.txt', '.doc')):
                obj = s3.get_object(Bucket=bucket_name, Key=file_key)
                file_content = obj['Body'].read()

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
                        text = read_doc_with_tika(io.BytesIO(file_content))
                    elif file_key.endswith('.txt'):
                        text = file_content.decode('utf-8', errors='ignore')
                        # print("*********8",text)

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
                                # pattern = r''.join([f"{c}[^ ]*" for c in
                                #                     term])  # Match term with optional characters after each letter
                                # partial_matches = re.findall(r'\b{}\b'.format(pattern), text)
                                # query_dict[term] += len(partial_matches)
                        else:
                            query_dict[term] += text.count(term)
                            # pattern = r''.join(
                            #     [f"{c}[^ ]*" for c in term])  # Match term with optional characters after each letter
                            # partial_matches = re.findall(r'\b{}\b'.format(pattern), text)
                            # query_dict[term] += len(partial_matches)
                    print("query_dict",query_dict)
                    groups_satisfied = all(count > 0 for count in query_dict.values())
                    similarity = calculate_similarity(jd, text)
                    print("file,similarity-1",file_key,similarity)
                    if groups_satisfied:
                        cnt+=1
                        exp = extract_experience(text)
                        similarity = calculate_similarity(jd,text)
                        print("file,similarity-2",file_key,exp)
                        matched_resumes.append((file_key, "file_path", query_dict, exp,similarity))  # Include exp in the tuple
                        # if cnt > 2:
                        #     break
                except Exception as e:
                    print(f"Error processing {file_key}: {e}")

                    # Your existing logic for processing the text and matching against the search query goes here

                #     similarity = calculate_similarity(jd, text)

                #     if similarity > 0.5:  # Example threshold for similarity score
                #         exp = extract_experience(text)
                #         matched_resumes.append((file_key, file_key, {}, exp, similarity))  # Placeholder values for query_dict and exp
                # except Exception as e:
                #     print(f"Error processing {file_key}: {e}")
                

    return matched_resumes

def create_excel(matched_resumes, output_file):
    if matched_resumes:
        wb = Workbook()
        ws = wb.active
        ws.append(["Resume", "Path", "Experience", "Score"])  # Add appropriate headers

        for resume in matched_resumes:
            ws.append([resume[0], resume[1], resume[3], resume[4]])  # Append relevant data

        wb.save(output_file)
        print("Excel file created successfully:", output_file)

# Example usage
bucket_name = 'resume-matcher-file'
search_query = 'Oracle and AWS'
access_key = 'AKIA2UC26RDVALSNC56M'
secret_key = 'Ehl3heDPxXdP5/F2TX7iDspBOD3PM1eQV2ay5amn'
output_file = 'matched_resumes.xlsx'
job_description = """Your job description here"""

matched_resumes = search_resumes(bucket_name, search_query, job_description, access_key, secret_key)
create_excel(matched_resumes, output_file)
