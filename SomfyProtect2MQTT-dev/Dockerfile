# https://developers.home-assistant.io/docs/add-ons/configuration#add-on-dockerfile
ARG BUILD_FROM
FROM ${BUILD_FROM}

ENV LANG=C.UTF-8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copy root filesystem
COPY rootfs /

# Setup base - Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libgl1 \
    libglib2.0-0 \
    libjxl-dev \
    libjxl-tools \
    libopus-dev \
    libsrtp2-dev \
    libvpx-dev \
    wget \
    yq \
    && rm -rf /var/lib/apt/lists/*

# Download source and untar
WORKDIR /usr/bin
ADD "https://github.com/Minims/SomfyProtect2MQTT/archive/refs/heads/dev.tar.gz" dev.tar.gz
RUN tar -xvf dev.tar.gz && mv /usr/bin/SomfyProtect2MQTT-dev /usr/bin/SomfyProtect2MQTT && rm dev.tar.gz

# Install python3 requirements
WORKDIR /usr/bin/SomfyProtect2MQTT/somfyProtect2Mqtt
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements/addon.txt
