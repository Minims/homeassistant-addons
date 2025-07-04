# Changelog

## 2025.7.0

fix: VisioPhone, write video to media folder.

## 2025.3.0

feature: allow video_backend change
fix: Somfy API breaking change since LINK Update to 2.13.0

## 2025.2.2

fix: config directory for go2rtc & echo
improve: history. First Run will published old messages.

## 2025.2.1c

fix: musl alpine dependency

## 2025.2.1b

fix: test armv7 libjxl

## 2025.2.1a

fix: installation / upgrade issue

## 2025.2.0

fix: restore 2025.1.0 version with fix for x86_64
feature: Add smoke binary sensor

## 2025.1.5

roolback: use somfyProtect2MQTT 2024.9.0
2025.1.0: moved to somfyProtect2MQTT-dev

## 2025.1.0

feature: Add videophone like v500 (ringing, snapshot, open gate, etc.)
feature: Add History
feature: Add Video Events
visiophone: write clip to /media folder
visiophone: save snapshot/video to media folder for visiophone
fix: try to use asyncio on websocket

## 2024.9.0

- fix: resubscribe to all topic on MQTT reconnect

## 2024.3.0

- fix: remove human_detect_enabled
- chore: set version to 2024.3.0
- feature: Add device_class motion for PIR and safety for IntelliTag

## 2024.1.0

- fix: default value for update_available

## 2023.12.2

- fix: Immediate Alarm Status on update

## 2023.12.1

- fix: reduce WebSocket time before restart

## 2023.12.0

- fix: Improve WebSocket
- chore: Update requirements

## 2023.11.0

- fix: do not ask for snapshot if shutter is closed

## 2023.10.0

- feature: Allow camera streaming via MQTT Camera OR WebRTC Camera (go2rtc)

## 2023.9.4

- fix: CPU Load

## 2023.9.3

- fix: MQTT True/False Command
- fix: restart process on failure

## 2023.9.2

- fix: supported_fetaures to 14
  https://github.com/Minims/SomfyProtect2MQTT/issues/55

  It won't be automatically fixed.
  You have to remove the alarm device first.
  Then restart the Addon.
  Update your lovelave entity & automatation.

  If i make the update on my side,
  the alarm device can change his name (installation before 2023.8.0)
  and it will break your automation & dashboard.

## 2023.9.1

- Fix: Test Siren buttons
- Feat: Add Beta Video Streaming
  https://github.com/Minims/SomfyProtect2MQTT#video-streaming

## 2023.8.3

- Add Watermark on snapshot

## 2023.8.2

- Test Siren buttons
- Update MQTT to feat HA 2023.8.0
- Improve WebSocket

## 2023.8.1

- Fix Load Issue
- Retain all MQTT Messages

## 2023.8.0

- Improve WebSocket messages

## 2023.7.0

- Update requirements
- Fix installation failure because of PyYaml

## 2023.6.1

- Clean old binary_sensor device_lost

## 2023.6.0

- Change Versioning to 2023.6.0
- Add some detailled log to debug
- Update Requirements
- Add scenarios in logs for some future features
- Improve WebSocket
- Breaking Change: update device_lost binary_sensor to device_tracker
- Fix Typo in device_lost / presence

## 0.2.9

- Fix ambient_light_threshold & smart_alarm_duration

## 0.2.8

- Fix smart_alarm_duration & lighting_trigger

## 0.2.7

- Wait 2 sec to upadte device after action.
- Add GET scenarios-core & scenario (for later usage)
- Update README
- Add Reboot / Halt button for Camera and Link
- Fix smart_alarm_duration

## 0.2.6

- Update device after action
- Update shutter_state switch
- Fix lighting_state switch
- Update lighting_state
- Add new sensors/switchs
- Add generic update device
- Add User api calls
- Add User Model
- Update Action List
- Update version to 0.2.6
- Remove signal_strength device_class on % signal

## 0.2.5

- Add Debug log on Site and Devices
- Add interndoor type

## 0.2.4

- Fix security.level.change

## 0.2.3

- Fix battery_low

## 0.2.2

- Fix recalibration_required

## 0.2.1

- Add IntellTag Motion Sensor (Alpha)
- Fix Update Device/Site

## 0.2.0

- Fix intellitag door type
- Fix camera video type
- Add Somfy One/One+
- Improve Logging

## 0.1.9.8

- Update Add-on to new S6: https://developers.home-assistant.io/blog/2022/05/12/s6-overlay-base-images/

## 0.1.9

- Add some new entities
- Fix Websocket Refresh Token
- Add motion sensor when alarm is triggered

## 0.1.8

- Add MQTT ssl
- Bump SomfyProtect2MQTT

## 0.1.7

- Fix request_token

## 0.1.6

- Add Manual Snapshot mode
- Add Old MyFox Security Camera
- Add Smoke Detector
- Add Extender
- Change default code value to 0

## 0.1.5

- Fix homeassistant_config schema

## 0.1.4

- Use SomfyProtect2MQTT 0.1.3
- Fix OutDoor Camera Snapshot
- Add possibilty to setup a code on alarm panel
- Allow to disable code on arm and/or disarm

## 0.1.3

- Use SomfyProtect2MQTT 0.1.2
- Fix Stop Alarm
- Fix Trigger Alarm
- Do not publish unwanted devices

## 0.1.2

- Add build.json file (thanks to @Minims)

## 0.1.1

- Changed tar link

## 0.1.0

- Addon renamed "SomfyProtect2MQTT-dev"
- Lot of code rewritten (thanks to @Minims)
- Based on dev branch
- Added logo, icon, changelog, docs...

## 0.0.1 to 0.0.4

- Initial version with minor fixes
