# FROM python:3.10-slim

# # Install the AWS Lambda Runtime Interface Client
# RUN pip install --no-cache-dir awslambdaric

# # Install build tools
# # RUN apt-get update && apt-get install -y build-essential gcc

# # Copy and install the dependenciesaws ecr get-login-password --region ap-southeast-2 | docker login --username AWS --password-stdin 730335185130.dkr.ecr.ap-southeast-2.amazonaws.com
# COPY requirements.txt ./
# RUN pip install -r requirements.txt


# # Copy the lambda function code
# COPY lambda_function.py ./

# # Set the command to run the Lambda function
# CMD ["lambda_function.lambda_handler"]
 


# # Use the official Python image from the slim version
# FROM python:3.10-slim

# # Install the AWS Lambda Runtime Interface Client
# RUN pip install --no-cache-dir awslambdaric

# # Copy and install the dependencies
# COPY requirements.txt ./
# RUN pip install -r requirements.txt

# # Copy the lambda function code
# COPY lambda_function.py ./

# # Set the command to run the Lambda function using the AWS Lambda Runtime Interface Client
# CMD ["python3", "-m", "awslambdaric", "lambda_function.lambda_handler"]


FROM python:3.10-slim

# Install the AWS Lambda Runtime Interface Client
RUN pip install --no-cache-dir awslambdaric

# Install additional required packages
# ADDED FOR THIS ERROR IN AWS     ----->    Error extracting text from 1714292849867.pdf: The file "b'%PDF-1.7\r\n%\xb5\xb5\xb5\xb5\r\n1 0 obj\r\n<</Type/Catalog/Pages 2 0 R/Lang(en) /StructTreeRoot 62 0 R/MarkInfo<</Marked true>>/Metadata 457 0 R/ViewerPreferences
RUN apt-get update && apt-get install -y \
    build-essential \
    libpoppler-cpp-dev \
    tesseract-ocr \
    poppler-utils

# Install Python dependencies
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Copy the lambda function code
COPY lambda_function.py ./

# Set the entry point to use the AWS Lambda Runtime Interface Emulator for local testing
# ENTRYPOINT ["python3", "-m", "awslambdaric"]

# Set the command to run the Lambda function using the AWS Lambda Runtime Interface Client
CMD ["python3", "-m", "awslambdaric", "lambda_function.lambda_handler"]
