FROM python:alpine

RUN apk update && \
    apk add --virtual build-deps gcc python-dev musl-dev && \
    apk add postgresql-dev

WORKDIR /tmp/wdir

ADD requirements.txt .

ADD api/ ./api

ADD setup.py .

RUN pip install . && cd / && rm -rf /tmp/wdir

ENTRYPOINT [ "job_api" ]
