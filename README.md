# Home Assistant Wii U Integration

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

![Project Maintenance][maintenance-shield]
<!-- [![BuyMeCoffee][buymecoffeebadge]][buymecoffee] -->

[![Discord][discord-shield]][discord]
[![Community Forum][forum-shield]][forum]

_Integration to integrate with a hacked [Wii U][Wii U] console with [Ristretto][Ristretto].

**This integration will set up the following platforms.**

Platform | Description
-- | --
`media_player` | Shows the current running title or application.
`button` | Restart console button.

## Installation

First, make sure you have [Ristretto][Ristretto] installed.

### HACS

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=ItzSwirlz&repository=ha-wiiu&category=integration)

### Manual

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
1. If you do not have a `custom_components` directory (folder) there, you need to create it.
1. In the `custom_components` directory (folder) create a new folder called `nintendo_wiiu_ristretto`.
1. Download _all_ the files from the `custom_components/nintendo_wiiu_ristretto/` directory (folder) in this repository.
1. Place the files you downloaded in the new directory (folder) you created.
1. Restart Home Assistant
1. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "Nintendo Wii U (with Ristretto)"

## Configuration is done in the UI

<!---->

## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

***

[Wii U]: https://github.com/ItzSwirlz/ha-wiiu
[Ristretto]: https://github.com/ItzSwirlz/Ristretto
<!-- [buymecoffee]: https://www.buymeacoffee.com/ItzSwirlz -->
<!-- [buymecoffeebadge]: https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg?style=for-the-badge -->
[commits-shield]: https://img.shields.io/github/commit-activity/y/ItzSwirlz/ha-wiiu.svg?style=for-the-badge
[commits]: https://github.com/ItzSwirlz/ha-wiiu/commits/main
[discord]: https://discord.gg/Qa5fW2R
[discord-shield]: https://img.shields.io/discord/330944238910963714.svg?style=for-the-badge
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=for-the-badge
[forum]: https://community.home-assistant.io/
[license-shield]: https://img.shields.io/github/license/ItzSwirlz/ha-wiiu.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-Joakim%20Sørensen%20%40ItzSwirlz-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/ItzSwirlz/ha-wiiu.svg?style=for-the-badge
[releases]: https://github.com/ItzSwirlz/ha-wiiu/releases
