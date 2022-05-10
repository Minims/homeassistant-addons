ARG BUILD_FROM
FROM $BUILD_FROM
ENV LANG C.UTF-8

# SomfyProtect2MQTT version
ARG VERSION=0.1.8
# Install required packages
RUN apk add --no-cache py3-pip
RUN pip3 install python-json2yaml

# Download source and untar
WORKDIR /usr/src
ADD "https://github.com/Minims/SomfyProtect2MQTT/archive/refs/tags/${VERSION}.tar.gz" src.tar.gz
RUN tar -xvf src.tar.gz
RUN mv /usr/src/SomfyProtect2MQTT-${VERSION} /usr/src/SomfyProtect2MQTT

# Install python requirements
WORKDIR /usr/src/SomfyProtect2MQTT/somfyProtect2Mqtt
RUN pip3 install -r requirements.txt

# Run script
COPY run.sh /
RUN chmod a+x /run.sh
CMD [ "/run.sh" ]
