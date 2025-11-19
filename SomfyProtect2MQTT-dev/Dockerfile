# https://developers.home-assistant.io/docs/add-ons/configuration#add-on-dockerfile
ARG BUILD_FROM
FROM ${BUILD_FROM}
ENV LANG=C.UTF-8

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
RUN tar -xvf dev.tar.gz && mv /usr/bin/SomfyProtect2MQTT-dev /usr/bin/SomfyProtect2MQTT && rm dev.tar.gz

# Install python3 requirements
WORKDIR /usr/bin/SomfyProtect2MQTT/somfyProtect2Mqtt

# Upgrade pip and setuptools, filter out opencv-python from requirements, then install
RUN pip3 install --no-cache-dir --break-system-packages --upgrade "pip>=24.0" "setuptools>=70.0" wheel && \
    grep -v "opencv-python" requirements/addon.txt > requirements_filtered.txt && \
    pip3 install --no-cache-dir --break-system-packages --prefer-binary -r requirements_filtered.txt
