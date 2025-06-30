# Use the standard AWS Lambda Python image
FROM public.ecr.aws/lambda/python:3.12

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy source code
COPY app.py .
COPY src/ ./src

# Lambda entrypoint
CMD ["app.lambda_handler"]