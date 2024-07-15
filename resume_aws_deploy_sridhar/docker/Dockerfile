# FROM public.ecr.aws/lambda/python:3.8

# COPY requirements.txt ./
# RUN pip3 install -r requirements.txt
# # # Install spaCy model
# RUN python -m spacy download en_core_web_lg
# COPY lambda_function.py ./

# CMD ["lambda_function.lambda_handler"]

# # Use a Python 3.11 base image from Docker Hub
# FROM python:3.11-slim

# # Install the AWS Lambda Runtime Interface Client
# RUN pip install --no-cache-dir awslambdaric

# # Copy and install the dependencies
# COPY requirements.txt ./
# RUN pip install -r requirements.txt

# # Install spaCy model
# RUN python -m spacy download en_core_web_lg

# # Copy the lambda function code
# COPY lambda_function.py ./

# # Set the command to run the Lambda function
# CMD ["lambda_function.lambda_handler"]


# # Use a Python 3.10 base image from Docker Hub
# FROM python:3.10-slim-bullseye
# Use a small base image
FROM python:3.10-slim

# Install the AWS Lambda Runtime Interface Client
RUN pip install --no-cache-dir awslambdaric

# Install build tools
RUN apt-get update && apt-get install -y build-essential gcc

# Copy and install the dependenciesaws ecr get-login-password --region ap-southeast-2 | docker login --username AWS --password-stdin 730335185130.dkr.ecr.ap-southeast-2.amazonaws.com
COPY requirements.txt ./
RUN pip install -r requirements.txt


# Copy the lambda function code
COPY lambda_function.py ./

# Set the command to run the Lambda function
CMD ["lambda_function.lambda_handler"]


# # Use a small base image
# FROM python:3.10-slim as base

# # Install build tools
# RUN apt-get update && apt-get install -y build-essential gcc

# # Create a builder stage
# FROM base as builder
# WORKDIR /app
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# # Final image
# FROM base
# COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
# COPY lambda_function.py ./
# CMD ["lambda_function.lambda_handler"]
