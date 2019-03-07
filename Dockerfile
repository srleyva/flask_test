FROM python:alpine

WORKDIR /tmp/wdir

ADD requirements.txt .

ADD api/ ./api

ADD setup.py .

RUN pip install . && cd / && rm -rf /tmp/wdir

ENTRYPOINT [ "job_api" ]