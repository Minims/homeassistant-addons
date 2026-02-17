# https://developers.home-assistant.io/docs/add-ons/configuration#add-on-dockerfile
ARG BUILD_FROM
# hadolint ignore=DL3006
FROM ${BUILD_FROM}
ENV LANG=C.UTF-8

# Install required packages
WORKDIR /usr/bin
# hadolint ignore=DL3018
RUN apk add --no-cache curl py3-pip \
    && pip3 install --no-cache-dir python-json2yaml==0.1.1 \
    && curl -fsSL "https://github.com/Minims/MyFox2MQTT/archive/refs/heads/dev.tar.gz" -o dev.tar.gz \
    && tar -xvf dev.tar.gz \
    && mv /usr/bin/MyFox2MQTT-dev /usr/bin/MyFox2MQTT \
    && rm -f dev.tar.gz \
    && pip3 install --no-cache-dir -r /usr/bin/MyFox2MQTT/myFox2Mqtt/requirements.txt

# Copy root filesystem
COPY rootfs /
