# https://developers.home-assistant.io/docs/add-ons/configuration#add-on-dockerfile
ARG BUILD_FROM
FROM ${BUILD_FROM}
ENV LANG C.UTF-8

# Copy root filesystem
COPY rootfs /

# Setup base
RUN apk update && apk add --no-cache \
    ffmpeg \
    ffmpeg-dev \
    libjxl \
    libjxl-tools \
    libsrtp \
    libsrtp-dev \
    libvpx \
    libvpx-dev \
    linux-headers \
    opus \
    opus-dev \
    py3-opencv \
    py3-pip \
    python3 \
    python3-dev \
    yq

# Download source and untar
WORKDIR /usr/bin
ADD "https://github.com/Minims/SomfyProtect2MQTT/archive/refs/heads/dev.tar.gz" dev.tar.gz
RUN tar -xvf dev.tar.gz && mv /usr/bin/SomfyProtect2MQTT-dev /usr/bin/SomfyProtect2MQTT

# Install python3 requirements
WORKDIR /usr/bin/SomfyProtect2MQTT/somfyProtect2Mqtt
RUN pip3 install --no-cache-dir -r requirements/addon.txt
