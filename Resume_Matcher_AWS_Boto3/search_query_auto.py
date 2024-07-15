# import spacy
# # def extract_search_query(job_description):
# #     # Load the spaCy model for NLP
# #     nlp = spacy.load("en_core_web_lg")

# #     # Process the job description text
# #     doc = nlp(job_description)

# #     # Extract nouns and verbs as keywords for the search query
# #     keywords = [token.text for token in doc if token.pos_ in ['NOUN', 'VERB']]

# #     # Join the keywords to form the search query
# #     search_query = ' '.join(keywords)

# #     return search_query

# # # Assume job_description is the text of the job description
# # job_description = "This is a job description that includes relevant keywords like AWS, SQL, Python, and data analysis."
# # search_query = extract_search_query(job_description)
# # print("Extracted Search Query:", search_query)

# def extract_skills(job_description):
#     # Load the spaCy model for NLP
#     nlp = spacy.load("en_core_web_lg")

#     # Process the job description text
#     doc = nlp(job_description)

#     # Extract entities that represent skills
#     skills = [ent.text for ent in doc.ents if ent.label_ == 'SKILL']

#     return skills

# # Assume job_description is the text of the job description
# job_description = "This is a job description that includes relevant keywords like AWS, SQL, Python, and data analysis."
# # skills = extract_skills(job_description)
# # print("Extracted Skills:", skills)

# from transformers import pipeline

# # Load the skill extraction pipeline
# skill_extraction = pipeline("zero-shot-classification", model="jjzha/jobbert_skill_extraction", tokenizer="jjzha/jobbert_skill_extraction")

# # Define a job description
# job_description = "This is a job description that includes relevant keywords like AWS, SQL, Python, and data analysis."

# # Extract skills from the job description
# result = skill_extraction(job_description, candidate_labels=["AWS", "SQL", "Python", "data analysis"], multi_class=True)

# # Get the predicted skills
# skills = result["labels"]

# print("Extracted Skills:", skills)



# from sklearn.feature_extraction.text import TfidfVectorizer
# import numpy as np

# # Sample job description text
# job_description = """
# We are looking for a software engineer with experience in Python, Java, and machine learning. 
# The ideal candidate should have strong problem-solving skills and experience with data analysis tools such as Pandas and NumPy.
# """

# # Preprocess the text (lowercase, remove punctuation, etc.)
# job_description = job_description.lower()  # Convert to lowercase
# # Add more preprocessing steps as needed

# # Create a TF-IDF vectorizer
# vectorizer = TfidfVectorizer()

# # Fit the vectorizer on the job description text
# vectorizer.fit([job_description])

# # Extract feature names (words) and their TF-IDF scores
# feature_names = vectorizer.get_feature_names_out()
# tfidf_scores = vectorizer.transform([job_description])

# # Sort feature names based on TF-IDF scores
# sorted_indices = tfidf_scores.indices[np.argsort(tfidf_scores.data)[::-1]]

# # Extract top keywords (skills)
# top_keywords = [feature_names[idx] for idx in sorted_indices[:10]]  # Extract top 10 keywords

# print("Top keywords extracted from job description:", top_keywords)


import spacy

# Load the spaCy model for NLP
nlp = spacy.load("en_core_web_lg")

def extract_search_query(job_description):
    # Process the job description text using spaCy
    doc = nlp(job_description)
    
    # Extract relevant keywords or phrases based on your criteria
    # For example, extracting nouns and noun phrases
    relevant_tokens = [token.text for token in doc if token.pos_ in ["NOUN", "PROPN"]]
    
    # Join the extracted tokens to form the search query
    search_query = ", ".join(relevant_tokens)
    
    return search_query

# Example job description
job_description = """
Andres Eduardo Cano
Laveen, AZ 85339 | Home: (602) 573-9516 | Andrescano30@yahoo.com
TECHNOLOGY LEADER
Dynamic technology leader with experience holding various senior leadership positions in Business Development,
Sales, Strategic Partner Alliances and Go-To-Market Growth, SaaS Marketplace, Marketplace, Professional
Services, Training and Development, and Program Management.  Knowledgeable in cloud computing (AWS,
Google, AZURE), ecommerce, Generative AI, IoT, Telematics.  Spearheading and nurturing strategic partner
development, growth and alliances, co-sell motions, account management, business development and market
research while growing vertical businesses in (education, finance, healthcare and life science, BPO, retail, and
nonprofit).  Developing strategic partnerships with ISV’s and GSI’s. Distributors, and Consulting partners within
verticals working with channel resellers. Proficient Native Spanish Speaker (Verbal, Written, and Read).
AREAS OF EXPERTISE
Project Management | Market Research & Strategic Partner Growth | Marketplace Development
Leadership | Data Analysis | Contract Negotiations | Business Development | Strategic Planning
Partner Enablement & Sales | SaaS & Sales | Global Data Privacy Regulations
PROFESSIONAL EXPERIENCE
Amazon Web Services, Phoenix AZ – Remote1/2024-Present
Sr. Manager, Public Sector – Education Partner Strategy – LATAM vertical leader
Lead education vertical strategy building co-sell & GTM motion with strategic partners at AWS delivering our
"""

# Extract the search query from the job description
search_query = extract_search_query(job_description)
print("Extracted Search Query:", search_query)
