# Home Assistant Add-on: SomfyProtect2MQTT-dev

## Installation

Follow these steps to get the add-on installed on your system:

1. Navigate in your Home Assistant frontend to **Supervisor** -> **Add-on Store**.
2. Find the "SomfyProtect2MQTT" add-on and click it.
3. Click on the "INSTALL" button.

## How to use

1. Perform the SomfyProtect2MQTT add-on configuration (see below)
2. Save the add-on configuration by clicking the "SAVE" button.
3. Start the add-on.

## Configuration

Add-on configuration:

```yaml
somfy_protect:
  username: mail@example.org
  password: iliketurtles
  sites:
    - Maison

homeassistant_config:
  code: "1234"
  code_arm_required: false
  code_disarm_required: true
  device_macs:
    - device: "<Somfy badge device ID or unique label>"
      mac: "AA:BB:CC:DD:EE:FF"

mqtt:
  host: 192.168.1.1
  port: "1883"
  ssl: false
  username: homeassistant
  password: homeassistant
  client-id: somfy-protect
  topic_prefix: somfyProtect2mqtt-dev
  ha_discover_prefix: homeassistant
delay_site: "10"
delay_device: "60"
manual_snapshot: false
streaming: mqtt
hls_host: 0.0.0.0
hls_port: 8090
debug: false
```

### Option group `somfy_protect`

The following options are for the option group: `somfy_protect`.

#### Options `username` and `password`

Username and password to use to authenticate to Somfy account.

#### Option `sites`

A list of sites to retrieve datas.

### Option group `homeassistant_config`

The following options are for the option group: `homeassistant_config`.

#### Option `code`

A code to arm/disarm in HA. Set to 0 to disable.

#### Option `code_arm_required`

Set to `false` if you want to arm without code

#### Option `code_disarm_required`

Set to `false` if you want to disarm without code

#### Option `device_macs`

Optional list used to associate Somfy badges with Bluetooth devices in Home Assistant. For each badge, set `device`
to its Somfy device ID when possible, or to its unique label, and set `mac` to the Bluetooth address shown as
`Address` in Home Assistant. Restart the add-on after changing this option so MQTT discovery is republished.

### Option group `mqtt`

The following options are for the option group: `mqtt`.

#### Options `host`, `port`, `ssl`, `username` and `password`

Host and credentials to use to authenticate to MQTT broker.

#### Option `client-id`

MQTT client identifier.

#### Option `topic_prefix`

MQTT prefix to use for data topic.

#### Option `ha_discover_prefix`

MQTT prefix to use for Home-Assistant discovery.

### Option `delay_site`

Define delay in seconds to update sites.

### Option `delay_device`

Define delay in seconds to update devices.

### Option `manual_snapshot`

Enable/Disable manual_snapshot.
false: Only update snapshot when switch 'snapshot' is triggered
true: snapshot auto update every 1min.

### Option `streaming`

Streaming Mode.
mqtt: Send image by image to MQTT camera in HA
go2rtc: write the url in /config/somfyprotect2mqtt/stream*url*<device_id>
to be read with echo source: https://github.com/AlexxIT/go2rtc#source-echo
and WebRTC Camera:https://github.com/AlexxIT/WebRTC

### Option `hls_host`

Address used by the HLS server. Keep `0.0.0.0` for the Home Assistant add-on.

### Option `hls_port`

Port used by the HLS server. The default is `8090`.

### Option `debug`

Enable/Disable debug mode.

## Runtime and development checks

The dev addon uses Python 3.14 from its Alpine base. Its Dockerfile pins the
SomfyProtect2MQTT commit; update `SOMFY_REF` when publishing a new dev build.
The image build checks native CRC32C and OpenCV's FFmpeg backend.

Generated configuration and the Somfy token cache are stored in `/data/config.yaml`
and `/data/token.json`. Configure the addon through Home Assistant's options.
The startup script does not print the configuration or credentials.

To test startup locally, install Python 3.14, Bash, and
[mikefarah/yq](https://github.com/mikefarah/yq), then run from the repository root:

```sh
python3 -m unittest discover -s SomfyProtect2MQTT-dev/tests -v
shellcheck SomfyProtect2MQTT-dev/rootfs/etc/s6-overlay/s6-rc.d/SomfyProtect2MQTT/{run,finish}
```

Tests use temporary files and a Supervisor stub; no Somfy account is needed.
