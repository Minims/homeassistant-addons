[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/minims)

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/minims)

# Minims Home Assistant add-on repository

[![Open your Home Assistant instance and show the add add-on repository dialog with a specific repository URL pre-filled.](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2FMinims%2Fhomeassistant-addons)

## Issues

- SomfyProtect2MQTT => https://github.com/Minims/SomfyProtect2MQTT/issues
- MyFox2MQTT => https://github.com/Minims/MyFox2MQTT/issues

## Manual Installation

Go to the _Supervisor_ Panel, select _Add-on Store_, click the three little dots on the upper right and select _Repositories_. Now fill the _Add repository_ textbox with `https://github.com/Minims/homeassistant-addons/` and click _Add_.

## Add-ons

This repository contains the following add-ons

### <img src="SomfyProtect2MQTT/icon.png" width="40px"> [SomfyProtect2MQTT add-on](./SomfyProtect2MQTT)

Publish Somfy Home Alarm as MQTT messages.

![Supports aarch64 Architecture][aarch64-shield]
![Supports amd64 Architecture][amd64-shield]

### <img src="SomfyProtect2MQTT-dev/icon.png" width="40px"> [SomfyProtect2MQTT-dev add-on](./SomfyProtect2MQTT-dev)

Publish Somfy Home Alarm as MQTT messages (dev version).

![Supports aarch64 Architecture][aarch64-shield]
![Supports amd64 Architecture][amd64-shield]

### <img src="SomfyProtect2MQTT-2nd-somfy-account/icon.png" width="40px"> [SomfyProtect2MQTT - 2nd Somfy Account add-on](./SomfyProtect2MQTT-2nd-somfy-account)

Publish Somfy Home Alarm as MQTT messages (2nd Somfy Account).

![Supports aarch64 Architecture][aarch64-shield]
![Supports amd64 Architecture][amd64-shield]

### <img src="MyFox2MQTT/icon.png" width="40px"> [MyFox2MQTT add-on](./MyFox2MQTT)

Publish MyFox Alarm as MQTT messages.

![Supports aarch64 Architecture][aarch64-shield]
![Supports amd64 Architecture][amd64-shield]

### <img src="MyFox2MQTT-dev/icon.png" width="40px"> [MyFox2MQTT-dev add-on](./MyFox2MQTT-dev)

Publish MyFox Alarm as MQTT messages (dev version).

![Supports aarch64 Architecture][aarch64-shield]
![Supports amd64 Architecture][amd64-shield]

<!--

Notes to developers after forking or using the github template feature:
- While developing comment out the 'image' key from 'example/config.yaml' to make the supervisor build the addon
  - Remember to put this back when pushing up your changes.
- When you merge to the 'main' branch of your repository a new build will be triggered.
  - Make sure you adjust the 'version' key in 'example/config.yaml' when you do that.
  - Make sure you update 'example/CHANGELOG.md' when you do that.
  - The first time this runs you might need to adjust the image configuration on github container registry to make it public
- Adjust the 'image' key in 'example/config.yaml' so it points to your username instead of 'home-assistant'.
  - This is where the build images will be published to.
- Rename the example directory.
  - The 'slug' key in 'example/config.yaml' should match the directory name.
- Adjust all keys/url's that points to 'home-assistant' to now point to your user/fork.
- Share your repository on the forums https://community.home-assistant.io/c/projects/9
- Do awesome stuff!
 -->

[aarch64-shield]: https://img.shields.io/badge/aarch64-yes-green.svg
[amd64-shield]: https://img.shields.io/badge/amd64-yes-green.svg

Many Thanks to [schumijo](https://github.com/schumijo) for his work on this addon !
