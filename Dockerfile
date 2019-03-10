FROM python:alpine

RUN apk update && \
    apk add --virtual build-deps gcc python-dev musl-dev && \
    apk add postgresql-dev

ENV API_LOGGING_CONF /etc/logging.conf

WORKDIR /tmp/wdir

ADD requirements.txt .

ADD api/ ./api

ADD setup.py .

RUN pip install . && cd / && rm -rf /tmp/wdir

ADD logging.conf /etc/

ENTRYPOINT [ "job_api" ]
