import spacy
import PyPDF2
import docx2txt
import textract
import re
import json
import boto3
from io import BytesIO
import os

# Load SpaCy model
nlp = spacy.load("en_core_web_trf")

# Initialize S3 client
s3 = boto3.client('s3')


# Function to extract text from different file types
def extract_text(file_path, file_ext):
    if file_ext == '.pdf':
        text = extract_text_from_pdf(file_path)
    elif file_ext == '.docx':
        text = extract_text_from_docx(file_path)
    elif file_ext == '.doc':
        text = textract.process(file_path).decode('utf-8')
    elif file_ext == '.txt':
        text = file_path.read().decode('utf-8')
    else:
        raise ValueError("Unsupported file type: {}".format(file_ext))
    return text


def extract_text_from_pdf(file_path):
    text = ""
    reader = PyPDF2.PdfReader(file_path)
    for page in reader.pages:
        text += page.extract_text()
    return text


def extract_text_from_docx(file_path):
    return docx2txt.process(file_path)


# Function to extract entities using SpaCy and custom rules
def extract_entities(text):
    doc = nlp(text)
    entities = {
        "name": [],
        "phone_number": [],
        "email": [],
        "clearances": [],
        "skills": []
    }

    phone_pattern = re.compile(r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b')
    email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')

    known_skills = [
        "Python", "SF Dev", "SF Admin", "Oracle", "SQL", "TOAD", "Java", "JavaScript",
        "TypeScript", "C++", "C#", "Ruby", "Go", "Swift", "Kotlin", "PHP", "R", "HTML",
        "CSS", "Angular", "React", "Vue.js", "Node.js", "Django", "Flask", "ASP.NET",
        "Spring", "iOS", "Android", "Flutter", "React Native", "MongoDB", "Cassandra",
        "Hadoop", "Spark", "Kafka", "ETL", "Data Warehousing", "AWS", "Azure", "Google Cloud",
        "Docker", "Kubernetes", "Terraform", "Jenkins", "Ansible", "Puppet", "Chef", "CI/CD",
        "TensorFlow", "PyTorch", "Scikit-learn", "Keras", "NLP", "Computer Vision", "Deep Learning",
        "Network Security", "Information Security", "Penetration Testing", "Incident Response",
        "SIEM", "Firewalls", "VPNs", "Solidity", "Ethereum", "Smart Contracts", "DeFi", "NFTs",
        "Hyperledger", "Low-code/no-code development", "Ethical hacking", "Quantum computing", 'C#', '.net'
    ]

    clearance_terms = ["dod", "public trust", "doj", "top secret clearance"]

    for ent in doc.ents:
        if ent.label_ == "PERSON":
            entities["name"].append(ent.text)
        if phone_pattern.match(ent.text):
            entities["phone_number"].append(ent.text)
        if email_pattern.match(ent.text):
            entities["email"].append(ent.text)
        if ent.text.lower() in clearance_terms:
            entities["clearances"].append(ent.text)
        if ent.label_ == "SKILL":
            entities["skills"].append(ent.text)

    for match in phone_pattern.findall(text):
        entities["phone_number"].append(match)
    for match in email_pattern.findall(text):
        entities["email"].append(match)

    possible_names = []
    for line in text.split("\n"):
        line = line.strip()
        if len(line.split()) == 2:  # Consider lines with only two words as potential names
            possible_names.append(line)
        elif "name" in line.lower():
            possible_names.append(line)

    for name in possible_names:
        doc = nlp(name)
        for ent in doc.ents:
            if ent.label_ == "PERSON" and name.lower() not in [entity.lower() for entity in entities["name"]]:
                entities["name"].append(name)

    for clearance in clearance_terms:
        if clearance in text.lower():
            entities["clearances"].append(clearance.capitalize())

    for skill in known_skills:
        if skill.lower() in text.lower():
            entities["skills"].append(skill)

    for key in entities:
        entities[key] = list(set(entities[key]))

    return entities


# Lambda handler function
def lambda_handler(event, context):
    bucket = event['bucket']
    key = event['key']

    # Get the file extension
    file_ext = os.path.splitext(key)[1].lower()

    # Download the file from S3
    s3_object = s3.get_object(Bucket=bucket, Key=key)
    file_content = BytesIO(s3_object['Body'].read())

    # Extract text and process resume
    text = extract_text(file_content, file_ext)
    entities = extract_entities(text)

    return {
        'statusCode': 200,
        'body': json.dumps(entities, indent=4)
    }
