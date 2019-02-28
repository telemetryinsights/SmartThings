# FUTURE: use a build like alpine to make this smaller and faster (one that includes python)
ARG BUILD_FROM=python:3.6-alpine
FROM $BUILD_FROM

ARG BUILD_ARCH
ARG BUILD_VERSION

LABEL authors="Homemations"

# install git and Python3 environment
RUN apk update \
 && apk add --no-cache git python3 \
 && python3 -m ensurepip \
 && rm -r /usr/lib/python*/ensurepip \
 && pip3 install --upgrade pip setuptools \
 && pip install --no-cache-dir -r requirements.txt \
 && cd /usr/bin \
 && ln -sf pip3 pip \
 && ln -sf python3 python \
 && rm -rf /root/.cache /var/cache

ADD . /app

WORKDIR /appy
CMD [ "python3", "radiora-classic-bridge.py" ]
