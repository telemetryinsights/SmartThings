ARG BUILD_FROM=homeassistant/amd64-base:latest
FROM $BUILD_FROM

LABEL authors="Stephen Harris <stephen@homemations.com>"

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


LABEL \
    io.hass.name="Lutron Radio RA1 Gateway" \
    io.hass.description="Play Spotify music on your Home Assistant device" \
    io.hass.arch="${BUILD_ARCH}" \
    io.hass.type="addon" \
    io.hass.version=${BUILD_VERSION} \
    org.label-schema.description="Play Spotify music on your Home Assistant device" \
    org.label-schema.build-date=${BUILD_DATE} \
    org.label-schema.name="Spotify Connect" \
    org.label-schema.schema-version="1.0" \
    org.label-schema.url="https://community.home-assistant.io/t/community-hass-io-add-on-spotify-connect/61210?u=frenck" \
    org.label-schema.usage="https://github.com/hassio-addons/addon-spotify-connect/tree/master/README.md" \
    org.label-schema.vcs-ref=${BUILD_REF} \
    org.label-schema.vcs-url="https://github.com/hassio-addons/addon-spotify-connect" \
    org.label-schema.vendor="Community Hass.io Add-ons"
