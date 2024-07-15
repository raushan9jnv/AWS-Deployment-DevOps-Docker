import requests
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
import json

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

def extract_entities(text):
    doc = nlp(text)
    entities = [ent.text.lower() for ent in doc.ents if ent.label_ in ['ORG', 'PRODUCT', 'WORK_OF_ART', 'TECH']]
    return list(set(entities))

def get_search_query(job_description):
    entities = extract_entities(job_description)
    return ', '.join(entities)

# def search_resumes(resume_data, search_query):
def search_resumes():
    matched_resumes = []
    cnt = 0
    print(cnt)

    auth_url = 'https://login.salesforce.com/services/oauth2/token'
    payload = {
            'grant_type': 'password',
            'client_id': '3',
            'client_secret': '',
            'username': '',
            'password': ''
        }
    response = requests.post(auth_url, data=payload)
    access_token = response.json()['access_token']

        # Salesforce API request to query Resume data
    api_url = 'https://ddl000000s9q9uak-dev-ed.develop.my.salesforce.com/services/data/v60.0/query/?q=SELECT+Resume_ID__c,Resume_Link__c,Job_Description__c+FROM+Resume__c'
    headers = {
            'Authorization': 'Bearer ' + access_token,
            'Content-Type': 'application/json'
        }
    response = requests.get(api_url, headers=headers)
        # print(response)
    resume_data = response.json()['records']
        # print(data)



    for record in resume_data:
        resume_id = record['resume_id__c']
        resume_link = record['resume_link__c']
        jd = record['job_description__c']
        print(resume_link)
        try:
            response = requests.get(resume_link)
            if response.status_code == 200:
                file_content = response.content
                text = ""
                # print(file_content)
                print(text)

                if resume_link.endswith('.pdf'):
                    pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))
                    num_pages = len(pdf_reader.pages)
                    for page_num in range(num_pages):
                        page = pdf_reader.pages[page_num]
                        text += page.extract_text()
                        # print("pdf------------",text)
                elif resume_link.endswith('.docx'):
                    text = docx2txt.process(io.BytesIO(file_content))
                    # print("docx--------",text)
                elif resume_link.endswith('.doc'):
                    text = read_doc_with_tika(file_content)
                elif resume_link.endswith('.txt'):
                    text = file_content.decode('utf-8', errors='ignore')

                text = text.lower()
                query_dict = {}
                search_query = get_search_query(jd)
                print("Extracted Search Query:", search_query)


                input_query = search_query.lower().replace('“', '').replace('”', '').replace('(', '').replace(')', '')
                # input_query_split = input_query.split("and")
                input_query_split = input_query.split(",")
                for item in input_query_split:
                    query_dict[item] = 0
                print("query_dict",query_dict)
                for term in query_dict.keys():
                    if term.__contains__("or"):
                        or_list = term.split("or")
                        for c in or_list:
                            query_dict[term] += text.count(c)
                    else:
                        query_dict[term] += text.count(term)
                groups_satisfied = all(count > 0 for count in query_dict.values())
                print("groups_satisfied---",groups_satisfied)
                similarity = calculate_similarity(jd, text)
                print("similarity------",similarity)
                if groups_satisfied:
                    print("groups_satisfied",groups_satisfied)
                    cnt += 1
                    exp = extract_experience(text)
                    similarity = calculate_similarity(jd,text)
                    matched_resumes.append({'id': resume_id, 'url': resume_link, 'query_matches': query_dict, 'experience': exp, 'similarity_score': similarity})
        except Exception as e:
            print(f"Error processing {resume_link}: {e}")

    return matched_resumes

def create_json(matched_resumes, output_file):
    
    for resume in matched_resumes:
        # Convert numpy float32 to Python float
        resume['similarity_score'] = float(resume['similarity_score'])
    with open(output_file, 'w') as json_file:
        json.dump(matched_resumes, json_file, indent=4)
        print("JSON file created successfully:", output_file)

 
output_file = 'matched_resumes.json'

    # Assume resume_data is the JSON data containing resume IDs and URLs
resume_data =[

    { "id":1,
    "resume_link": "https://pivotalleap-salesforce.s3.amazonaws.com/SalesforceResumeAttachments/Latestrequirments.docx",
    "job_description": """Job Title: Senior Security Architect and Engineer

Job Description:

We are seeking a highly skilled and experienced Senior Security Architect and Engineer to join our team. The ideal candidate will have a diverse background in security operations, firewall architecture, vulnerability management, and cloud security tools administration. As a key member of our team, you will be responsible for designing, implementing, and maintaining robust security solutions to protect our organization's assets from cyber threats.

Key Responsibilities:
 """
    },


    {
    "id":2,
     "resume_link": "https://pivotalleap-salesforce.s3.amazonaws.com/SalesforceResumeAttachments/AndresCano.pdf",
     "job_description": "hello test 2"
    }
]

# matched_resumes = search_resumes(resume_data, search_query)
matched_resumes = search_resumes()
create_json(matched_resumes, output_file)
