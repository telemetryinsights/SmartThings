ARG BUILD_FROM=homeassistant/amd64-base:latest
FROM $BUILD_FROM

LABEL authors="Stephen Harris <stephen@homemations.com>"

# Install node and npm
RUN apk update -y \
 && apk add --no-cache --virtual bash \
 && apk add --no-cache python-pip python-dev

# Install HomeMation's latest Lutron RadioRA Manager
#
# NOTE: the SmartThings Groovy handlers are also downloaded so that we can
# show them in the HASS add-on configuration view and we ensure that the
# version used matches the version of the Python (in case something changes
# at the same time).
#
#RUN git clone \
#  https://github.com/homemations/SmartThings/tree/master/Lutron%20RadioRA \
#  "Lutron RadioRA"
COPY ../lutron /app

#COPY ./requirements.txt /app/requirements.txt
COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

ENTRYPOINT [ "python" ]
CMD [ "lutronapp.py" ]

# Build arguments
ARG BUILD_ARCH
ARG BUILD_DATE
ARG BUILD_REF
ARG BUILD_VERSION

LABEL \
    io.hass.name="Lutron Radio RA1 SmartThings Gateway" \
    io.hass.description="Gateway between SmartThings and Lutron RadioRA 1 RS-232 serial controller" \
    io.hass.arch="${BUILD_ARCH}" \
    io.hass.type="addon" \
    io.hass.version=${BUILD_VERSION} \
    org.label-schema.description="Gateway between SmartThings and Lutron RadioRA 1 RS-232 serial controller" \
    org.label-schema.build-date=${BUILD_DATE} \
    org.label-schema.name="Lutron Radio RA1 SmartThings Gateway" \
    org.label-schema.schema-version="1.0" \
    org.label-schema.url="https://community.home-assistant.io/t/community-hass-io-add-on-lutron-radiora/" \
    org.label-schema.usage="https://github.com/rsnodgrass/SmartThings/Lutron%20RadioRA/hassio/README.md" \
    org.label-schema.vcs-ref=${BUILD_REF} \
    org.label-schema.vcs-url="https://github.com/rsnodgrass/SmartThings/tree/master/Lutron%20RadioRA/hassio \
    org.label-schema.vendor="Community Hass.io Add-ons"
