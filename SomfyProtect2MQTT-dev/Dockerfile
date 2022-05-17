# https://developers.home-assistant.io/docs/add-ons/configuration#add-on-dockerfile
ARG BUILD_FROM
FROM $BUILD_FROM
ENV LANG C.UTF-8

# Install required packages
RUN apk add --no-cache py3-pip
RUN pip3 install python-json2yaml

# Download source and untar
WORKDIR /usr/bin
ADD "https://github.com/Minims/SomfyProtect2MQTT/archive/refs/heads/dev.tar.gz" dev.tar.gz
RUN tar -xvf dev.tar.gz
RUN mv /usr/bin/SomfyProtect2MQTT-dev /usr/bin/SomfyProtect2MQTT

# Install python3 requirements
WORKDIR /usr/bin/SomfyProtect2MQTT/somfyProtect2Mqtt
RUN pip3 install -r requirements.txt

# Copy root filesystem
COPY rootfs /
