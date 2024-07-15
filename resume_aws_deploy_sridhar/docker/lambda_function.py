import re
# import os
import logging
import hashlib
import string
import boto3
from io import BytesIO
from langchain_community.document_loaders import TextLoader, PyPDFLoader, Docx2txtLoader
import chromadb
from chromadb.utils import embedding_functions
import time

logging.basicConfig(level=logging.INFO)

ef = embedding_functions.DefaultEmbeddingFunction()

def clean_text(doc_text):
    doc_text = re.sub(r'\s+', ' ', doc_text.strip())
    doc_text = re.sub(r'\n+', '\n', doc_text.strip()).strip('\n')
    doc_text = doc_text.replace("\xa0", "")
    doc_text = re.sub(r'\s+([' + re.escape(string.punctuation) + r'])', r'\1', doc_text)
    doc_text = re.sub(r'[^\x20-\x7E]', '', doc_text)
    return doc_text

class ChromaDB:
    def __init__(self, name):
        self.docs = []
        self.chroma_client = chromadb.PersistentClient(path=".chroma")
        self.collection = self.chroma_client.get_or_create_collection(
            name=name, metadata={"hnsw:space": "cosine"}, embedding_function=ef
        )

    def add_resumes(self, resume_list):
        new_docs = []
        for filename, file_content in resume_list:
            try:
                if filename.endswith(".pdf"):
                    doc = PyPDFLoader(BytesIO(file_content)).load()
                elif filename.endswith(".docx"):
                    doc = Docx2txtLoader(BytesIO(file_content)).load()
                elif filename.endswith(".txt"):
                    doc = TextLoader(BytesIO(file_content), encoding='utf-8').load()
                else:
                    continue

                doc_text = ""
                for page_no, page in enumerate(doc):
                    doc_text += clean_text(page.page_content) + " "

                doc_hash = self.get_hash(doc_text)

                existing_docs = self.collection.get(ids=[doc_hash], include=["documents", "metadatas"])
                if existing_docs["documents"]:
                    continue

                new_docs.append({
                    "doc": doc_text,
                    "filename": filename,
                    "hash": doc_hash
                })
            except Exception as e:
                logging.error(f"Unable to add {filename} due to {str(e)}")

        self.docs.extend(new_docs)
        self._index_documents()

    def _index_documents(self):
        if not self.docs:
            logging.warning("No documents to index.")
            return

        texts = []
        ids = []
        metadatas = []

        for doc in self.docs:
            texts.append(doc["doc"])
            ids.append(str(doc["hash"]))
            metadatas.append({
                "doc_hash": doc["hash"],
                "doc_filename": doc["filename"]
            })

        self.collection.add(documents=texts, ids=ids, metadatas=metadatas)

    def query_resumes(self, keyword, job_description, n_results=10):
        query_text = clean_text(keyword + " " + job_description)
        results = self.collection.query(
            query_texts=[query_text],
            include=["documents", "distances", "metadatas"],
            n_results=n_results
        )

        distances = results["distances"][0]
        ids = results["ids"][0]
        documents = results["documents"][0]

        filtered_results = []
        for i in range(len(distances)):
            filtered_results.append({
                "filename": results["metadatas"][0][i]["doc_filename"],
                "distance": distances[i],
                "document": documents[i]
            })

        filtered_results.sort(key=lambda x: x["distance"])

        return filtered_results[:n_results]

    def get_hash(self, document_text, algorithm="sha256"):
        hash_object = hashlib.new(algorithm)
        hash_object.update(document_text.encode("utf-8"))
        document_hash = hash_object.hexdigest()
        return document_hash

def lambda_handler(event, context):
    s3_bucket_name = event["s3_bucket_name"]
    job_description = event["job_description"]
    search_query = event["search_query"]

    s3_client = boto3.client('s3')
    bucket_objects = s3_client.list_objects_v2(Bucket=s3_bucket_name)

    if 'Contents' not in bucket_objects:
        logging.warning("No files found in the S3 bucket.")
        return

    resume_files = []
    for obj in bucket_objects['Contents']:
        file_key = obj['Key']
        file_obj = s3_client.get_object(Bucket=s3_bucket_name, Key=file_key)
        file_content = file_obj['Body'].read()
        resume_files.append((file_key, file_content))

    db = ChromaDB(name="resumes_collection")
    db.add_resumes(resume_files)

    start_time = time.time()
    matching_resumes = db.query_resumes(search_query, job_description, n_results=10)

    top_resumes = [{"Resume": resume['filename'], "Score": resume['distance']} for resume in matching_resumes]

    logging.info("Top matching resumes:")
    for resume in top_resumes:
        logging.info(f"Resume: {resume['Resume']}, Score: {resume['Score']}")

    end_time = time.time()
    total_time = end_time - start_time
    logging.info(f"Total time taken: {total_time:.2f} seconds")

    return {
        "statusCode": 200,
        "body": top_resumes
    }
