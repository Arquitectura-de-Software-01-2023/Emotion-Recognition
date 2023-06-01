FROM --platform=linux/amd64 public.ecr.aws/lambda/python:3.8

COPY app.py ./
COPY ai/ ./ai/
COPY requirements.txt ./

RUN yum update -y
RUN pip install -r requirements.txt
RUN yum install -y mesa-libGL

CMD ["app.handler"]
