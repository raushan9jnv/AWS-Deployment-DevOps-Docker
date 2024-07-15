import spacy

# Load the English language model
nlp = spacy.load("en_core_web_lg")

# # Sample job description text
# job_description ="""
# Andres Eduardo Cano
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
# """

# # Process the job description text
# doc = nlp(job_description)

# # Extract skills using named entity recognition (NER) and nouns
# skills = []
# for ent in doc.ents:
#     if ent.label_ == "PRODUCT" or ent.label_ == "ORG":  # Filter out product and organization entities
#         skills.append(ent.text)
# for token in doc:
#     if token.pos_ == "NOUN":  # Check if token is a noun
#         skills.append(token.text)

# # Remove duplicates
# skills = list(set(skills))

# # Print extracted skills
# print("Skills extracted from job description:", skills)

def extract_entities(text):
    doc = nlp(text)
    entities = [ent.text.lower() for ent in doc.ents if ent.label_ in ['ORG', 'PRODUCT', 'WORK_OF_ART', 'TECH']]
    return list(set(entities))

def get_search_query(job_description):
    entities = extract_entities(job_description)
    return ', '.join(entities)

# Now, modify the main part of the code to use the extracted search query:
job_description = '''We seek a highly skilled and experienced Senior RPA Developer. The ideal candidate will design, develop, and implement RPA systems to automate business processes, increase efficiency, reduce errors. The role requires advanced UiPath platform capabilities
UiPath Document Understanding • UiPath DU Taxonomy, Digitization, Document Classification, Extraction, Validation, Consumption Configurations • UiPath AI Center • UiPath ML Training and Learning Models, including pipelines. • UiPath Action Center / Human-In-the-loop design and development UiPath Orchestrator Administration • UiPath Orchestrator configuration and admin • Deployment of versioned UiPath modules to production UiPath Insights UiPath Insights dashboard architecture, design development, and support Key Responsibilities: • Lead the design, development, and implementation of RPA solutions to automate business processes. • Work closely with business analysts, process owners, QA analysts, and other cross-functional resources to understand the business requirements and workflows. • Develop and configure RPA processes and objects using core workflow principles in an efficient and scalable manner. • Conduct thorough testing of RPA solutions, ensuring robustness and reliability. Qualifications: • Bachelor’s degree in computer science, Information Technology, or a related field. • Minimum of 5 years of experience in RPA development, with a proven track record of successful project delivery. • Minimum of 2 years of experience and strength, specifically with UiPath automation architecture • Strong expertise in RPA tools such as UiPath, Blue Prism, Automation Anywhere, etc. • Proficiency in programming languages such as C#, .NET, Java, Python, .Net, JS, or others.
• Experience with Databases (SQL or NoSQL) is often preferred. • Excellent understanding of workflow-based logic and the ability to both understand a business process from a workflow diagram and to conceptualize it as an automated solution. • Experience with process analysis, design, and implementation; business and technical requirements analysis; project management. • Strong problem-solving and analytical skills. • Excellent communication and interpersonal skills, with the ability to work effectively with team members, stakeholders, and clients. • Certification in RPA tools is a plus.• Manage the deployment of RPA components, including bots, robots, and development tools. • Integrate RPA BOT’s with ITSM Help desk ticketing system to ensure robust exception handling to proper support levels. • Build and maintain Operational Dashboards with performance and other operational efficiency statistics. • Provide technical leadership and guidance to junior RPA developers. • Monitor the performance of RPA solutions utilizing UiPath Orchestrator and make admin adjustments as necessary to ensure optimal efficiency. • Document the RPA development process, including Process Capture (PDD), design (SDD) documentation, configuration, testing, and deployment details. • Stay current with the latest RPA technologies and best practices and incorporate them into our processes.
Skill Matrix:
Bachelor’s degree in computer science, Information Technology, or a related field.
Minimum of 5 years of experience in RPA development, with a proven track record of successful project delivery.----------5 years
Minimum of 2 years of experience and strength, specifically with UiPath automation architecture----------2 years
Strong expertise in RPA tools such as UiPath, Blue Prism, Automation Anywhere, etc
Proficiency in programming languages such as C#, .NET, Java, Python, .Net, JS, or others.
Experience with Databases (SQL or NoSQL) is often preferred.----Desired
 
'''

search_query = get_search_query(job_description)
print("Extracted Search Query:", search_query)

