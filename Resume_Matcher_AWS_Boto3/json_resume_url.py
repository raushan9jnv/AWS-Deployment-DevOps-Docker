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
def search_resumes(resume_data):
    matched_resumes = []
    cnt = 0
    print(cnt)

    for entry in resume_data:
        resume_id = entry['id']
        resume_link = entry['resume_link']
        jd = entry['job_description']
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

# def lambda_handler(event, context):
#     bucket_name = os.getenv('BUCKET_NAME') #'resume-matcher-file'
#     search_query = os.getenv('SEARCH_QUERY') #'Oracle and AWS'
#     job_description = os.getenv('JOB_DESCRIPTION') #"""Your job description here"""
#     output_file = 'matched_resumes.json'

#     # Assume resume_data is the JSON data containing resume IDs and URLs
#     resume_data = event['resume_data']

#     matched_resumes = search_resumes(resume_data, job_description)
#     create_json(matched_resumes, output_file)
 
    # bucket_name = os.getenv('BUCKET_NAME') #'resume-matcher-file'
# search_query = 'aws, python'
# job_description = """Andres Eduardo Cano
# Laveen, AZ 85339 | Home: (602) 573-9516 | Andrescano30@yahoo.com
# TECHNOLOGY LEADER
# Dynamic technology leader with experience holding various senior leadership positions in Business Development,
# Sales, Strategic Partner Alliances and Go-To-Market Growth, SaaS Marketplace, Marketplace, Professional
# Services, Training and Development, and Program Management.  Knowledgeable in cloud computing (AWS,
# Google, AZURE), ecommerce, Generative AI, IoT, Telematics.  Spearheading and nurturing strategic partner
# development, growth and alliances, co-sell motions, account management, business development and market
# research while growing vertical businesses in (education, finance, healthcare and life science, BPO, retail, and
# nonprofit).  Developing strategic partnerships with ISV’s and GSI’s. Distributors, and Consulting partners within
# verticals working with channel resellers. Proficient Native Spanish Speaker (Verbal, Written, and Read).
# AREAS OF EXPERTISE
# Project Management | Market Research & Strategic Partner Growth | Marketplace Development
# Leadership | Data Analysis | Contract Negotiations | Business Development | Strategic Planning
# Partner Enablement & Sales | SaaS & Sales | Global Data Privacy Regulations
# PROFESSIONAL EXPERIENCE
# Amazon Web Services, Phoenix AZ – Remote1/2024-Present
# Sr. Manager, Public Sector – Education Partner Strategy – LATAM vertical leader
# Lead education vertical strategy building co-sell & GTM motion with strategic partners at AWS delivering our
#  """
output_file = 'matched_resumes.json'

    # Assume resume_data is the JSON data containing resume IDs and URLs
resume_data =[

    { "id":1,
    "resume_link": "https://pivotalleap-salesforce.s3.amazonaws.com/SalesforceResumeAttachments/Latestrequirments.docx",
    "job_description": """Job Title: Senior Security Architect and Engineer

Job Description:

We are seeking a highly skilled and experienced Senior Security Architect and Engineer to join our team. The ideal candidate will have a diverse background in security operations, firewall architecture, vulnerability management, and cloud security tools administration. As a key member of our team, you will be responsible for designing, implementing, and maintaining robust security solutions to protect our organization's assets from cyber threats.

Key Responsibilities:

Security Architecture Design: Design and implement comprehensive security architectures to safeguard the organization's networks, systems, and data. This includes firewall architecture, network segmentation, and cloud security architecture.

Security Operations and Administration: Lead security operations, including vulnerability management, patch management, and incident response. Manage and maintain security tools such as SIEM, endpoint security, and web application firewalls.

Firewall Policy Management: Oversee firewall policy management across various platforms including Palo Alto, Checkpoint, Cisco ASA, and Fortinet. Ensure firewall policies align with industry best practices and regulatory requirements.

Cloud Security Administration: Administer and optimize cloud security tools and services in AWS and Azure environments. This includes AWS IAM, AWS WAF, Security Hub, CloudTrail, and Azure WAF.

Vulnerability Management: Manage and organize vulnerability scanning, assessment, and remediation efforts globally. Utilize tools such as Rapid7 InsightVM, Nessus, and AWS Trusted Advisor to identify and mitigate security vulnerabilities.

Incident Response: Lead cybersecurity incident response efforts, utilizing tools like Darktrace Enterprise Immune and coordinating with internal teams and external stakeholders to contain and mitigate security incidents.

Security Standards and Compliance: Ensure compliance with industry standards such as ISO27002, PCI DSS, and regulatory requirements like HIPAA and SOX. Implement and enforce security controls to meet compliance objectives.

Team Collaboration and Communication: Foster a collaborative and communicative environment within the security team and across diverse groups within the organization. Mentor junior team members and provide technical guidance as needed.

Qualifications:

Bachelor's degree in Computer Science, Information Technology, or related field.
Extensive experience (10+ years) in security architecture, engineering, and operations.
Strong proficiency in firewall architecture and administration across multiple platforms.
In-depth knowledge of cloud security tools and services in AWS and Azure environments.
Hands-on experience with vulnerability management tools such as Rapid7 InsightVM and Nessus.
Familiarity with security standards and compliance frameworks (e.g., ISO27002, PCI DSS).
Excellent communication and interpersonal skills, with the ability to collaborate effectively within teams and across departments.
Relevant certifications such as Palo Alto Networks ACE/ASE, CISSP, or equivalent certifications are highly desirable.
Note: This job description is intended to convey information essential to understanding the scope of the position and is not an exhaustive list of skills, efforts, duties, responsibilities, or working conditions associated with it."""
    },


    {
    "id":2,
     "resume_link": "https://pivotalleap-salesforce.s3.amazonaws.com/SalesforceResumeAttachments/AndresCano.pdf",
     "job_description": "hello test 2"
    }
]

# matched_resumes = search_resumes(resume_data, search_query)
matched_resumes = search_resumes(resume_data)
create_json(matched_resumes, output_file)
