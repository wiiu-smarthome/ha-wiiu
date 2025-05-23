"""Ristretto trigger dispatcher."""

from __future__ import annotations

from typing import TYPE_CHECKING, cast

from homeassistant.const import CONF_PLATFORM

from .triggers import turn_on

if TYPE_CHECKING:
    from homeassistant.core import CALLBACK_TYPE, HomeAssistant
    from homeassistant.helpers.trigger import (
        TriggerActionType,
        TriggerInfo,
        TriggerProtocol,
    )
    from homeassistant.helpers.typing import ConfigType

TRIGGERS = {
    "turn_on": turn_on,
}


def _get_trigger_platform(config: ConfigType) -> TriggerProtocol:
    """Return trigger platform."""
    platform_split = config[CONF_PLATFORM].split(".", maxsplit=1)
    if len(platform_split) < 2 or platform_split[1] not in TRIGGERS:  # noqa: PLR2004
        msg = f"Unknown Ristretto trigger platform {config[CONF_PLATFORM]}"
        raise ValueError(msg)
    return cast("TriggerProtocol", TRIGGERS[platform_split[1]])


async def async_validate_trigger_config(
    hass: HomeAssistant,  # noqa: ARG001
    config: ConfigType,
) -> ConfigType:
    """Validate config."""
    platform = _get_trigger_platform(config)
    return cast("ConfigType", platform.TRIGGER_SCHEMA(config))


async def async_attach_trigger(
    hass: HomeAssistant,
    config: ConfigType,
    action: TriggerActionType,
    trigger_info: TriggerInfo,
) -> CALLBACK_TYPE:
    """Attach trigger of specified platform."""
    platform = _get_trigger_platform(config)
    return await platform.async_attach_trigger(hass, config, action, trigger_info)
