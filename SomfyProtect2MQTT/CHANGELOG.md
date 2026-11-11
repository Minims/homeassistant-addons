# Changelog

## 2026.11.5 (dev)

- Fixed: Retry server-initiated WebRTC hang-ups with bounded 2, 5 and 15 second backoff
- Fixed: Cancel stale WebRTC retries when a newer session starts or the add-on shuts down
- Fixed: Align HLS audio startup with the first decoded video frame
- Fixed: Limit repeated H264 startup warnings while preserving other decoder errors
- Added: Document go2rtc AAC-to-Opus audio conversion for WebRTC playback

## 2026.11.4 (dev)

- Fixed: Use matching video frame and encoder time bases so HLS segments have correct playback timing
- Fixed: Send HTTP content lengths for HLS playlists and segments to avoid premature-end errors in players
- Fixed: Drain queued audio frames and render timestamps outside the network event loop to preserve synchronization under load
- Added: Live HLS timing, audio/video synchronization and HTTP response tests in addon image builds

## 2026.11.3 (dev)

- Updated: Pin SomfyProtect2MQTT 2026.11.3 and validate the Python 3.14 runtime
- Fixed: Serialize WebRTC shutdown and drain pending asynchronous tasks before closing the event loop
- Fixed: Keep generated configuration and the Somfy token in persistent `/data` storage
- Fixed: Preserve special characters in MQTT credentials and stop printing configuration secrets
- Fixed: Build the native CRC32C extension and use the current s6 user bundle directory
- Added: Startup regression tests and amd64/arm64 image checks, including native HLS codecs

## 2026.11.2 (dev)

- Fixed: Replace deprecated `build.yaml` with Dockerfile build settings and migrate the `addon_config` map type to `app_config`, preserving the mount path

## 2026.11.1 (dev)

- Updated: Add-on base image from `20.0.1` to `21.0.10` for amd64 and aarch64
- Added: MQTT availability reporting when the Somfy API cannot be reached, with recovery when connectivity returns
- Fixed: Isolate WebRTC sessions and reset HLS resources after hangup so streaming can restart

## 2026.11.0 (dev)

- Added: SOS button per site in Home Assistant using Somfy's silent panic mode
- Fixed: Preserve the triggered alarm state during periodic refreshes while an alarm is in progress ([#272](https://github.com/Minims/SomfyProtect2MQTT/pull/272))
- Fixed: Prevent outdated API responses from overwriting newer alarm or security events during concurrent updates

## 2026.10.0

- Added: Expose history attributes through MQTT JSON attributes
- Fixed: Publish history events from oldest to newest

## 2026.9.0

- Added: Expose device MAC connections in Home Assistant MQTT discovery
- Added: Associate Somfy badges with Bluetooth devices using `homeassistant_config.device_macs`
- Fixed: Distinguish Bluetooth addresses from network MAC connections
- Fixed: Invalid generated YAML when configuring badge Bluetooth addresses

## 2026.8.3

- Fixed: config folder permission error and rate-limit lock contention ([#268](https://github.com/Minims/SomfyProtect2MQTT/pull/268))

## 2026.8.2

- Fixed: Migrate existing numeric alarm codes to text without blocking add-on updates

## 2026.8.1

- Fixed: WebRTC streaming stability by reusing the site's TURN credential ([#263](https://github.com/Minims/SomfyProtect2MQTT/pull/263))
- Fixed: Preserve leading zeroes in Home Assistant alarm codes ([#266](https://github.com/Minims/SomfyProtect2MQTT/pull/266))

## 2026.8.0

- Fixed: go2rtc HLS segment generation
- Added: Configurable HLS server host and port

## 2026.4.0

- Fixed: SSO fallback on OAuth refresh errors

## 2026.3.1

- Fixed: Somfy SSO token rate-limit handling (retry-after honored, retry/backoff, improved logs)
- Fixed: MQTT startup broker connection context logging (host/port/ssl) with clearer init failure

## 2026.3.0

- Refactor: Major codebase refactor
- Fixed: Issues [#241](https://github.com/Minims/SomfyProtect2MQTT/issues/241), [#240](https://github.com/Minims/SomfyProtect2MQTT/issues/240), [#239](https://github.com/Minims/SomfyProtect2MQTT/issues/239)

## 2026.1.1

- Fixed: Boolean conversion [#236](https://github.com/Minims/SomfyProtect2MQTT/issues/236)

## 2026.1.0

- Fixed: No file descriptor available
- Fixed: Manually trigger alarm
- Breaking: WebRTC stream changed from MJPEG to HLS with audio
- Added: HLS stream for WebRTC cameras (`http://0.0.0.0:8090/<device_id>/playlist.m3u8`)

## 2025.12.4

- Fixed: WebRTC stream errors

## 2025.12.3

- Fixed: Authentication issue

## 2025.12.2

- Added: WebRTC stream support

## 2025.12.1

- Changed: Use MQTT Home Assistant Addon by default if MQTT config is missing
- Improved: Async updates for Site & Devices actions
- Added: DoorLock, update device on lock/unlock trigger
- Fixed: IndoorCamera night vision

## 2025.12.0

- Added: DoorLock, more sensors

## 2025.7.0

- Fixed: VisioPhone, write video to media folder

## 2025.3.0

- Added: Video backend change option
- Fixed: Somfy API breaking change (LINK Update 2.13.0)

## 2025.2.2

- Fixed: Config directory for go2rtc & echo
- Improved: History, first run publishes old messages

## 2025.2.1c

- Fixed: musl alpine dependency

## 2025.2.1b

- Fixed: Test armv7 libjxl

## 2025.2.1a

- Fixed: Installation/upgrade issue

## 2025.2.0

- Fixed: Restore 2025.1.0 version with x86_64 fix
- Added: Smoke binary sensor

## 2025.1.5

- Rolled back: Use SomfyProtect2MQTT 2024.9.0
- Changed: Moved to SomfyProtect2MQTT-dev

## 2025.1.0

- Added: Videophone (ringing, snapshot, open gate, etc.)
- Added: History
- Added: Video events
- Improved: VisioPhone, write clips and snapshots to media folder
- Fixed: Use asyncio for websocket

## 2024.9.0

- Fixed: Resubscribe to all topics on MQTT reconnect

## 2024.3.0

- Fixed: Remove human_detect_enabled
- Changed: Set version to 2024.3.0
- Added: Device class motion for PIR, safety for IntelliTag

## 2024.1.0

- Fixed: Default value for update_available

## 2023.12.2

- Fixed: Immediate alarm status on update

## 2023.12.1

- Fixed: Reduce WebSocket restart time

## 2023.12.0

- Improved: WebSocket
- Updated: Requirements

## 2023.11.0

- Fixed: Do not request snapshot if shutter is closed

## 2023.10.0

- Added: Camera streaming via MQTT Camera or WebRTC Camera (go2rtc)

## 2023.9.4

- Fixed: CPU load

## 2023.9.3

- Fixed: MQTT True/False command
- Fixed: Restart process on failure

## 2023.9.2

- Fixed: supported_features to 14 ([#55](https://github.com/Minims/SomfyProtect2MQTT/issues/55))
  - Manual intervention required: Remove alarm device, restart addon, update Lovelace entity & automation

## 2023.9.1

- Fixed: Siren buttons
- Added: Beta video streaming ([Video Streaming](https://github.com/Minims/SomfyProtect2MQTT#video-streaming))

## 2023.8.3

- Added: Watermark on snapshot

## 2023.8.2

- Added: Siren buttons
- Updated: MQTT for HA 2023.8.0
- Improved: WebSocket

## 2023.8.1

- Fixed: Load issue
- Changed: Retain all MQTT messages

## 2023.8.0

- Improved: WebSocket messages

## 2023.7.0

- Updated: Requirements
- Fixed: Installation failure (PyYaml)

## 2023.6.1

- Cleaned: Old binary_sensor device_lost

## 2023.6.0

- Changed: Versioning to 2023.6.0
- Added: Detailed logs for debugging
- Updated: Requirements
- Added: Scenarios in logs for future features
- Improved: WebSocket
- Breaking: device_lost binary_sensor updated to device_tracker
- Fixed: Typo in device_lost/presence

## 0.2.9

- Fixed: ambient_light_threshold & smart_alarm_duration

## 0.2.8

- Fixed: smart_alarm_duration & lighting_trigger

## 0.2.7

- Changed: Wait 2 sec to update device after action
- Added: GET scenarios-core & scenario (future use)
- Updated: README
- Added: Reboot/Halt button for Camera and Link
- Fixed: smart_alarm_duration

## 0.2.6

- Updated: Device after action
- Updated: shutter_state switch
- Fixed: lighting_state switch
- Updated: lighting_state
- Added: New sensors/switches
- Added: Generic update device
- Added: User API calls and model
- Updated: Action list
- Changed: Version to 0.2.6
- Removed: signal_strength device_class on % signal

## 0.2.5

- Added: Debug log on Site and Devices
- Added: interndoor type

## 0.2.4

- Fixed: security.level.change

## 0.2.3

- Fixed: battery_low

## 0.2.2

- Fixed: recalibration_required

## 0.2.1

- Added: IntelliTag motion sensor (alpha)
- Fixed: Update device/site

## 0.2.0

- Fixed: IntelliTag door type
- Fixed: Camera video type
- Added: Somfy One/One+
- Improved: Logging

## 0.1.9.8

- Updated: Add-on to new S6 ([S6 Overlay Base Images](https://developers.home-assistant.io/blog/2022/05/12/s6-overlay-base-images/))

## 0.1.9

- Added: New entities
- Fixed: WebSocket refresh token
- Added: Motion sensor when alarm is triggered

## 0.1.8

- Added: MQTT SSL
- Updated: SomfyProtect2MQTT

## 0.1.7

- Fixed: request_token

## 0.1.6

- Added: Manual snapshot mode
- Added: Old MyFox security camera
- Added: Smoke detector
- Added: Extender
- Changed: Default code value to 0

## 0.1.5

- Fixed: homeassistant_config schema

## 0.1.4

- Updated: SomfyProtect2MQTT 0.1.3
- Fixed: Outdoor camera snapshot
- Added: Setup code on alarm panel
- Allowed: Disable code on arm/disarm

## 0.1.3

- Updated: SomfyProtect2MQTT 0.1.2
- Fixed: Stop alarm
- Fixed: Trigger alarm
- Do not publish unwanted devices

## 0.1.2

- Added: build.json file (thanks @Minims)

## 0.1.1

- Changed: tar link

## 0.1.0

- Renamed: Addon to "SomfyProtect2MQTT-dev"
- Rewritten: Major code changes (thanks @Minims)
- Based on dev branch
- Added: Logo, icon, changelog, docs

## 0.0.1 to 0.0.4

- Initial version with minor fixes
