# https://developers.home-assistant.io/docs/add-ons/configuration#add-on-dockerfile
ARG BUILD_FROM
FROM ${BUILD_FROM}
ENV LANG=C.UTF-8

# Copy root filesystem
COPY rootfs /

# Do not compile packages from source
ENV PIP_NO_BUILD_ISOLATION=1
ENV PIP_PREFER_BINARY=1

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
    py3-cffi \
    py3-cryptography \
    py3-pip \
    python3 \
    python3-dev \
    yq

# Fix Alpine dist-info version strings so pip can parse them
RUN python3 - <<'PY'
from pathlib import Path
import site

for base in map(Path, site.getsitepackages()):
    if not base.exists():
        continue
    for meta in base.rglob("*.dist-info/METADATA"):
        text = meta.read_text()
        if "Version: python-" in text:
            meta.write_text(text.replace("Version: python-", "Version: "))
PY

# Download source and untar
WORKDIR /usr/bin
ADD "https://github.com/Minims/SomfyProtect2MQTT/archive/refs/heads/dev.tar.gz" dev.tar.gz
RUN tar -xvf dev.tar.gz && mv /usr/bin/SomfyProtect2MQTT-dev /usr/bin/SomfyProtect2MQTT

# Install python3 requirements
WORKDIR /usr/bin/SomfyProtect2MQTT/somfyProtect2Mqtt
RUN pip3 install --no-cache-dir --retries 5 --resume-retries 5 --timeout 120 -r requirements/addon.txt

# Install opencv after pip to avoid invalid version metadata crash
RUN apk add --no-cache py3-opencv
