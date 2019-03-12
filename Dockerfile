FROM sleyva97/gevent-base

ENV API_LOGGING_CONF /etc/logging.conf

WORKDIR /tmp/wdir

ADD requirements.txt .

ADD api/ ./api

ADD setup.py .

RUN pip install . && cd / && rm -rf /tmp/wdir

ADD logging.conf /etc/

ENTRYPOINT [ "job_api" ]
