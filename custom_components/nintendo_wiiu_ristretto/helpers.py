"""Helper functions for Nintendo WiiU Ristretto."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.config_entries import ConfigEntryState
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers import entity_registry as er

from .const import DOMAIN

if TYPE_CHECKING:
    from homeassistant.helpers.device_registry import DeviceEntry

    from .coordinator import WiiUCoordinator


@callback
def async_get_device_entry_by_device_id(
    hass: HomeAssistant, device_id: str
) -> DeviceEntry:
    """
    Get Device Entry from Device Registry by device ID.

    Raises ValueError if device ID is invalid.
    """
    device_reg = dr.async_get(hass)
    if (device := device_reg.async_get(device_id)) is None:
        msg = f"Device {device_id} is not a valid {DOMAIN} device."
        raise ValueError(msg)

    return device


@callback
def async_get_device_id_from_entity_id(hass: HomeAssistant, entity_id: str) -> str:
    """
    Get device ID from an entity ID.

    Raises ValueError if entity or device ID is invalid.
    """
    ent_reg = er.async_get(hass)
    entity_entry = ent_reg.async_get(entity_id)

    if (
        entity_entry is None
        or entity_entry.device_id is None
        or entity_entry.platform != DOMAIN
    ):
        msg = f"Entity {entity_id} is not a valid {DOMAIN} entity."
        raise ValueError(msg)

    return entity_entry.device_id


@callback
def async_get_client_by_device_entry(
    hass: HomeAssistant, device: DeviceEntry
) -> WiiUCoordinator:
    """
    Get WiiUCoordinator from Device Registry by device entry.

    Raises ValueError if client is not found.
    """
    entry: WiiUCoordinator | None
    for config_entry_id in device.config_entries:
        entry = hass.config_entries.async_get_entry(config_entry_id)
        if entry and entry.domain == DOMAIN and entry.state is ConfigEntryState.LOADED:
            return entry.runtime_data

    msg = f"Device {device.id} is not from an existing {DOMAIN} config entry"
    raise ValueError(msg)
