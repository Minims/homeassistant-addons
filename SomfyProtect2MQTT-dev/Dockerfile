# https://developers.home-assistant.io/docs/add-ons/configuration#add-on-dockerfile
ARG BUILD_FROM
FROM $BUILD_FROM
ENV LANG C.UTF-8

# Install required packages
RUN apk update --no-cache
RUN apk upgrade --no-cache
RUN apk add --no-cache py3-pip py3-opencv ffmpeg libjxl-tools libjxl yq openssl openssl-dev libsrtp libsrtp-dev libvpx libvpx-dev opus opus-dev ffmpeg-dev python3-dev build-base
# Download source and untar
WORKDIR /usr/bin
ADD "https://github.com/Minims/SomfyProtect2MQTT/archive/refs/heads/dev.tar.gz" dev.tar.gz
RUN tar -xvf dev.tar.gz
RUN mv /usr/bin/SomfyProtect2MQTT-dev /usr/bin/SomfyProtect2MQTT

# Install python3 requirements
WORKDIR /usr/bin/SomfyProtect2MQTT/somfyProtect2Mqtt
RUN pip3 install --no-cache-dir -r requirements/addon.txt

# Copy root filesystem
ADD rootfs /
