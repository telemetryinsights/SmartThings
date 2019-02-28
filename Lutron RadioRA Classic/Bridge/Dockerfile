# FUTURE: use a build like alpine to make this smaller and faster (one that includes python)
ARG BUILD_FROM=python:3.6-alpine
FROM $BUILD_FROM

ARG BUILD_ARCH
ARG BUILD_VERSION

LABEL authors="Homemations"

ADD . /app
WORKDIR /app

# install git and Python3 environment
RUN apk update \
 && apk add --no-cache python3 \
 && python3 -m ensurepip \
 && rm -r /usr/lib/python*/ensurepip \
 && pip3 install --upgrade pip setuptools \
 && pip install --no-cache-dir -r /app/requirements.txt \
 && cd /usr/bin \
 && ln -sf pip3 pip \
 && ln -sf python3 python \
 && rm -rf /root/.cache /var/cache \
 && TIMESTAMP="2019-02-26-00-00"

#CMD [ "python3", "radiora-classic-bridge.py" ]
CMD [ "/app/run.sh" ]
