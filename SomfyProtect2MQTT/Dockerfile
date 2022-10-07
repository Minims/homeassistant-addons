# https://developers.home-assistant.io/docs/add-ons/configuration#add-on-dockerfile
ARG BUILD_FROM
FROM $BUILD_FROM
ENV LANG C.UTF-8

# SomfyProtect2MQTT version
ARG VERSION=0.2.2

# Install required packages
RUN apk add --no-cache py3-pip
RUN pip3 install python-json2yaml

# Download source and untar
WORKDIR /usr/bin
ADD "https://github.com/Minims/SomfyProtect2MQTT/archive/refs/tags/${VERSION}.tar.gz" ${VERSION}.tar.gz
RUN tar -xvf ${VERSION}.tar.gz
RUN mv /usr/bin/SomfyProtect2MQTT-${VERSION} /usr/bin/SomfyProtect2MQTT

# Install python3 requirements
WORKDIR /usr/bin/SomfyProtect2MQTT/somfyProtect2Mqtt
RUN pip3 install -r requirements.txt

# Copy root filesystem
COPY rootfs /
