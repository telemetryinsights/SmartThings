ARG BUILD_FROM=homeassistant/amd64-base:latest
FROM $BUILD_FROM

# Install node and npm
RUN apk update -y \
 && apk add --no-cache --virtual bash git \
 && apk add --no-cache python-pip python-dev

# Install Homemation's latest Lutron RadioRA Manager
#
# NOTE: the SmartThings Groovy handlers are also downloaded so that we can
# show them in the HASS add-on configuration view and we ensure that the
# version used matches the version of the Python (in case something changes
# at the same time).
#
#RUN git clone \
#  https://github.com/homemations/SmartThings/tree/master/Lutron%20RadioRA \
#  "Lutron RadioRA"
COPY ../../lutron /app

#COPY ./requirements.txt /app/requirements.txt
COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

ENTRYPOINT [ "python" ]
CMD [ "lutronapp.py" ]

# docker run -d -p 8080:8080 lutron-radiora1 