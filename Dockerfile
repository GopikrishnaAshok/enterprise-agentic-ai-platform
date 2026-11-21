FROM public.ecr.aws/lambda/python:3.12

WORKDIR ${LAMBDA_TASK_ROOT}

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt


RUN python -c "import boto3, botocore; c=boto3.client('bedrock-agent-runtime',region_name='us-east-1'); s=c.meta.service_model.operation_model('Retrieve').input_shape.members['retrievalConfiguration'].members; print('boto3:',boto3.__version__,'botocore:',botocore.__version__,'supported:',list(s)); assert 'managedSearchConfiguration' in s, 'SDK does not support managedSearchConfiguration'"

COPY backend/ ./backend/
COPY memory/ ./memory/

CMD ["backend.app.lambda_handler.lambda_handler"]
