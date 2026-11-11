# https://developers.home-assistant.io/docs/add-ons/configuration#add-on-dockerfile
ARG BUILD_FROM=ghcr.io/hassio-addons/base:21.0.10
FROM ${BUILD_FROM}
LABEL org.opencontainers.image.title="Home Assistant Add-on: SomfyProtect2MQTT (dev)" \
      org.opencontainers.image.description="Publish Somfy Home Alarm as MQTT messages - Development branch." \
      org.opencontainers.image.source="https://github.com/Minims/homeassistant-addons" \
      org.opencontainers.image.licenses="Apache License 2.0"
ENV LANG=C.UTF-8

# Copy root filesystem
COPY rootfs /

# Prefer wheels except for CRC32C, which needs a native musl build.
ENV PIP_PREFER_BINARY=1

# Setup base
RUN apk update && apk add --no-cache \
    crc32c \
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

# Pin the tested dev revision so rebuilding the addon uses the same code.
ARG SOMFY_REF=c8f28409a3fb47c1cc09f168d8549f7841917585
ADD "https://github.com/Minims/SomfyProtect2MQTT/archive/${SOMFY_REF}.tar.gz" /tmp/somfy.tar.gz
RUN mkdir -p /usr/bin/SomfyProtect2MQTT \
    && tar -xzf /tmp/somfy.tar.gz --strip-components=1 -C /usr/bin/SomfyProtect2MQTT \
    && rm /tmp/somfy.tar.gz

# Install python3 requirements
WORKDIR /usr/bin/SomfyProtect2MQTT/somfyProtect2Mqtt
RUN apk add --no-cache --virtual .crc32c-build build-base crc32c-dev \
    && CRC32C_PURE_PYTHON=0 pip3 install --no-cache-dir --no-binary=google-crc32c \
        --retries 5 --resume-retries 5 --timeout 120 -r requirements/addon.txt \
    && pip3 check \
    && apk del .crc32c-build

# Install opencv after pip to avoid invalid version metadata crash
RUN apk add --no-cache py3-opencv

# Fail the build if the addon runtime drifts or a native backend cannot load.
RUN python3 - <<'PYTHON'
import sys
import runpy
import aiortc
import av
import cv2
import google_crc32c
assert sys.version_info[:2] == (3, 14), sys.version
assert google_crc32c.implementation == "c", "CRC32C native extension is missing"
assert google_crc32c.value(b"123456789") == 0xE3069283
assert cv2.videoio_registry.hasBackend(cv2.CAP_FFMPEG), "OpenCV FFmpeg backend is missing"
codec_tests = runpy.run_path("tests/test_media_codecs.py")
codec_tests["test_hls_segment_encodes_and_decodes_video_and_audio"]()
codec_tests["test_live_hls_video_timestamps_match_playlist_durations"]()
codec_tests["test_live_hls_audio_and_video_stay_synchronized"]()
runpy.run_path("tests/test_hls_http.py")["test_hls_responses_advertise_the_complete_body_length"]()
print(f"Python {sys.version.split()[0]}, aiortc {aiortc.__version__}, PyAV {av.__version__}, OpenCV {cv2.__version__}")
PYTHON
