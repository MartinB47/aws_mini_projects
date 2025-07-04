# Use the standard AWS Lambda Python image
FROM public.ecr.aws/lambda/python:3.12

# Copy requirements
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Copy source code
COPY src/ ./src

# Lambda entrypoint
CMD ["src.app.lambda_handler"]