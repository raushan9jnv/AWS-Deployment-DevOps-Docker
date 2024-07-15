from datetime import datetime
import os
import docx2txt
import PyPDF2
from openpyxl import Workbook
import re
import spacy
from sklearn.metrics.pairwise import cosine_similarity
from tika import parser

 #pre-trained spaCy model for natural language processing (NLP)
 # download it via "python -m spacy download en_core_web_lg"
nlp = spacy.load("en_core_web_lg")

def extract_experience(resume_text):
    # Sample pattern for extracting years of experience
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

def search_resumes(directory, search_query,jd):
    matched_resumes = []
    cnt = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(('.pdf', '.docx', '.txt','.doc')):
                print("doc")
                file_path = os.path.join(root, file)
                text = ""

                try:
                    # Read text from different file types
                    if file.endswith('.pdf'):
                        try:
                            with open(file_path, 'rb') as pdf_file:
                                reader = PyPDF2.PdfReader(pdf_file)
                                for page_num in range(len(reader.pages)):
                                    text += reader.pages[page_num].extract_text()
                        except Exception as e:
                            print(f"Error processing {file}: {e}")
                            continue

                    elif file.endswith('.docx'):
                        try:
                            text = docx2txt.process(file_path)
                        except Exception as e:
                            print(f"Error processing {file}: {e}")
                            continue
                    elif file.endswith('.doc'):
                        text = read_doc_with_tika(file_path)

                    elif file.endswith('.txt'):
                        with open(file_path, 'r', encoding='utf-8') as txt_file:
                            text = txt_file.read()
                    text = text.lower()
                    #print("pdf",text)
                    input_query = (search_query
                                   .replace('“', '')
                                   .replace('”', '')
                                   .replace('(', '')
                                   .replace(')','')
                                   .lower())
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
                    print("file,similarity-1",file,similarity)
                    if groups_satisfied:
                        cnt+=1
                        exp = extract_experience(text)
                        similarity = calculate_similarity(jd,text)
                        print("file,similarity-2",file,exp)
                        matched_resumes.append((file, file_path, query_dict, exp,similarity))  # Include exp in the tuple
                        # if cnt > 2:
                        #     break
                except Exception as e:
                    print(f"Error processing {file}: {e}")

    return matched_resumes


def create_excel(matched_resumes, output_file):
    if matched_resumes.__len__() != 0:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        output_file_with_timestamp = f"{output_file.split('.')[0]}_{timestamp}.xlsx"
        wb = Workbook()
        ws = wb.active
        ws.append(["Resume", "Path"] + list(matched_resumes[0][2].keys()) + ["Experience"] + ["Score"])  # Add "Experience" column

       # sorted_resumes = sorted(matched_resumes, key=lambda x: sum(x[2].values()), reverse=True)
        sorted_resumes = sorted(matched_resumes, key=lambda x: x[4], reverse=True)

        for resume in sorted_resumes:
            ws.append([resume[0], resume[1]] + list(resume[2].values()) + [resume[3]] + [resume[4]])  # Append experience information

        wb.save(output_file_with_timestamp)
        print("Excel file created successfully:", output_file_with_timestamp)


# search_query = "DBA and Oracle and Postgresql and AWS and 19C"
search_query = "Oracle and AWS"
directory_path = r"C:\\Users\\KAUSHAL KUMAR\\Downloads\\resume"
#directory_path = "D:\\Downloads\\Rahul Resume-20240211T113121Z-001\\Rahul Resume"
output_file = "matched_resumes.xlsx"
Job_Desciption = """Job Title: Senior Security Architect and Engineer

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

matched_resumes = search_resumes(directory_path, search_query,Job_Desciption)
print(matched_resumes)
create_excel(matched_resumes, output_file)