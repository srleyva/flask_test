FROM alpine

RUN apk add --upgrade postgresql-client git bash

WORKDIR /tmp/wdir

RUN git clone https://github.com/sstephenson/bats.git && \
	cd bats && \
 	./install.sh /usr/local

ADD structure.sql .
ADD populate.sql .
ADD test.sh .

ENTRYPOINT [ "./test.sh" ]
