# https://developers.home-assistant.io/docs/add-ons/configuration#add-on-dockerfile
ARG BUILD_FROM
# hadolint ignore=DL3006
FROM ${BUILD_FROM}
ENV LANG=C.UTF-8

# MyFox2MQTT version
ARG VERSION=2024.9.2

# Install required packages
WORKDIR /usr/bin
# hadolint ignore=DL3018
RUN apk add --no-cache curl py3-pip \
    && pip3 install --no-cache-dir python-json2yaml==0.1.1 \
    && curl -fsSL "https://github.com/Minims/MyFox2MQTT/archive/refs/tags/${VERSION}.tar.gz" -o "${VERSION}.tar.gz" \
    && tar -xvf "${VERSION}.tar.gz" \
    && mv "/usr/bin/MyFox2MQTT-${VERSION}" /usr/bin/MyFox2MQTT \
    && rm -f "${VERSION}.tar.gz" \
    && pip3 install --no-cache-dir -r /usr/bin/MyFox2MQTT/myFox2Mqtt/requirements.txt

# Copy root filesystem
COPY rootfs /
