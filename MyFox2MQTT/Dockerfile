# https://developers.home-assistant.io/docs/add-ons/configuration#add-on-dockerfile
ARG BUILD_FROM
FROM $BUILD_FROM
ENV LANG C.UTF-8

# MyFox2MQTT version
ARG VERSION=2024.9.2

# Install required packages
RUN apk add --no-cache py3-pip
RUN pip3 install --no-cache-dir python-json2yaml==0.1.1

# Download source and untar
WORKDIR /usr/bin
ADD "https://github.com/Minims/MyFox2MQTT/archive/refs/tags/${VERSION}.tar.gz" ${VERSION}.tar.gz
RUN tar -xvf ${VERSION}.tar.gz
RUN mv /usr/bin/MyFox2MQTT-${VERSION} /usr/bin/MyFox2MQTT

# Install python3 requirements
WORKDIR /usr/bin/MyFox2MQTT/myFox2Mqtt
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy root filesystem
ADD rootfs /
