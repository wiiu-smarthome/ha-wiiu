"""Nintendo WiiU Ristretto device trigger."""

from __future__ import annotations

from typing import TYPE_CHECKING

import voluptuous as vol
from homeassistant.components.device_automation import (
    DEVICE_TRIGGER_BASE_SCHEMA,
    InvalidDeviceAutomationConfig,
)
from homeassistant.const import CONF_DEVICE_ID, CONF_PLATFORM, CONF_TYPE
from homeassistant.exceptions import HomeAssistantError

from . import trigger
from .const import DOMAIN
from .helpers import (
    async_get_client_by_device_entry,
    async_get_device_entry_by_device_id,
)
from .triggers.turn_on import PLATFORM_TYPE as TURN_ON_PLATFORM_TYPE
from .triggers.turn_on import async_get_turn_on_trigger

if TYPE_CHECKING:
    from homeassistant.core import CALLBACK_TYPE, HomeAssistant
    from homeassistant.helpers.trigger import TriggerActionType, TriggerInfo
    from homeassistant.helpers.typing import ConfigType

TRIGGER_TYPES = {TURN_ON_PLATFORM_TYPE}
TRIGGER_SCHEMA = DEVICE_TRIGGER_BASE_SCHEMA.extend(
    {
        vol.Required(CONF_TYPE): vol.In(TRIGGER_TYPES),
    }
)


async def async_validate_trigger_config(
    hass: HomeAssistant, config: ConfigType
) -> ConfigType:
    """Validate config."""
    config = TRIGGER_SCHEMA(config)

    if config[CONF_TYPE] == TURN_ON_PLATFORM_TYPE:
        device_id = config[CONF_DEVICE_ID]
        try:
            device = async_get_device_entry_by_device_id(hass, device_id)
            async_get_client_by_device_entry(hass, device)
        except ValueError as err:
            raise InvalidDeviceAutomationConfig(err) from err

    return config


async def async_get_triggers(
    _hass: HomeAssistant, device_id: str
) -> list[dict[str, str]]:
    """List device triggers for device."""
    return [async_get_turn_on_trigger(device_id)]


async def async_attach_trigger(
    hass: HomeAssistant,
    config: ConfigType,
    action: TriggerActionType,
    trigger_info: TriggerInfo,
) -> CALLBACK_TYPE:
    """Attach a trigger."""
    if (trigger_type := config[CONF_TYPE]) == TURN_ON_PLATFORM_TYPE:
        trigger_config = {
            CONF_PLATFORM: trigger_type,
            CONF_DEVICE_ID: config[CONF_DEVICE_ID],
        }
        trigger_config = await trigger.async_validate_trigger_config(
            hass, trigger_config
        )
        return await trigger.async_attach_trigger(
            hass, trigger_config, action, trigger_info
        )

    raise HomeAssistantError(
        translation_domain=DOMAIN,
        translation_key="unhandled_trigger_type",
        translation_placeholders={"trigger_type": trigger_type},
    )
