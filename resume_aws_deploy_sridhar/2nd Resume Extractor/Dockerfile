FROM python:3.10-slim

# Install the AWS Lambda Runtime Interface Client
RUN pip install --no-cache-dir awslambdaric

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpoppler-cpp-dev \
    tesseract-ocr \
    poppler-utils \
    antiword \
    wget

# Install spaCy and additional transformer-based dependencies
RUN pip install spacy torch transformers

# Download spaCy transformer model
RUN python -m spacy download en_core_web_trf

# Install Python dependencies from requirements.txt
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Copy the lambda function code
COPY lambda_function.py ./

# Set the command to run the Lambda function using the AWS Lambda Runtime Interface Client
CMD ["python3", "-m", "awslambdaric", "lambda_function.lambda_handler"]
