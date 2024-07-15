# FROM public.ecr.aws/lambda/python:3.8

# COPY requirements.txt ./
# RUN pip3 install -r requirements.txt
# # # Install spaCy model
# RUN python -m spacy download en_core_web_lg
# COPY lambda_function.py ./

# CMD ["lambda_function.lambda_handler"]

# Use a Python 3.11 base image from Docker Hub
FROM python:3.11-slim

# Install the AWS Lambda Runtime Interface Client
RUN pip install --no-cache-dir awslambdaric

# Copy and install the dependencies
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Install spaCy model
RUN python -m spacy download en_core_web_lg

# Copy the lambda function code
COPY lambda_function.py ./

# Set the command to run the Lambda function
CMD ["lambda_function.lambda_handler"]
