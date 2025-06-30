# use the AL2023‐based Python 3.12 Lambda image
FROM public.ecr.aws/lambda/python:3.12       

# install system libs via microdnf instead of yum
RUN microdnf install -y gcc gfortran libpng-devel freetype-devel \
 && microdnf clean all

# Python deps
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Source code
COPY app.py .
COPY src/ ./src

# Lambda entrypoint
CMD ["app.lambda_handler"]