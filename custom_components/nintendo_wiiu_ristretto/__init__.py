"""Initialization."""

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .coordinator import WiiUCoordinator

PLATFORMS = [Platform.BUTTON, Platform.MEDIA_PLAYER, Platform.SENSOR]


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
