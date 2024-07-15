# FROM python:3.10-slim

# # Install the AWS Lambda Runtime Interface Client
# RUN pip install --no-cache-dir awslambdaric

# # Install additional required packages
#  RUN apt-get update && apt-get install -y \
#     build-essential \
#     libpoppler-cpp-dev \
#     tesseract-ocr \
#     poppler-utils

# # Install Python dependencies
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
RUN apt-get update && apt-get install -y \
    build-essential \
    libpoppler-cpp-dev \
    tesseract-ocr \
    poppler-utils \
    antiword \
    wget

# Install Python dependencies
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Copy the lambda function code
COPY lambda_function.py ./

# Set the command to run the Lambda function using the AWS Lambda Runtime Interface Client
CMD ["python3", "-m", "awslambdaric", "lambda_function.lambda_handler"]


