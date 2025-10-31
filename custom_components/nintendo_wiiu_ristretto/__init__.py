"""Initialization."""

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    ATTR_HW_VERSION,
    ATTR_MODEL,
    ATTR_SERIAL_NUMBER,
    ATTR_SW_VERSION,
    CONF_IP_ADDRESS,
    CONF_PORT,
    CONF_TIMEOUT,
    Platform,
)
from homeassistant.core import HomeAssistant

from .config_flow import get_device_info
from .const import DEFAULT_TIMEOUT
from .coordinator import WiiUCoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS = [
    Platform.BUTTON,
    Platform.MEDIA_PLAYER,
    Platform.SENSOR,
    Platform.BINARY_SENSOR,
]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Entry setup."""
    coordinator = WiiUCoordinator(hass=hass, config_entry=entry)

    entry.runtime_data = coordinator
    await coordinator.async_config_entry_first_refresh()

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Entry unloading."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

async def async_migrate_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Migrate a config entry to a new version."""
    if entry.version == 1:
        # Make a connection to load the required attributes
        try:
            serial, hw_version, model, sw_version = await get_device_info(
                hass=hass,
                ip_addres=entry.data[CONF_IP_ADDRESS],
                port=entry.data[CONF_PORT],
                timeout=entry.data.get(CONF_TIMEOUT, DEFAULT_TIMEOUT),
            )
        except (TimeoutError, ConnectionError):
            _LOGGER.exception(
                "Migration will only work if the Wii U is powered on."
            )
            return False
        else:
            new_data = {
                ATTR_HW_VERSION: hw_version,
                ATTR_MODEL: model,
                ATTR_SERIAL_NUMBER: serial,
                ATTR_SW_VERSION: sw_version,
                **entry.data
            }
            await hass.config_entries.async_update_entry(
                entry, data=new_data, version=2
            )
            return True
    return True
