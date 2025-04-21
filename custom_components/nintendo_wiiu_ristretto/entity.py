"""Base entity for a Wii U device."""

import logging

from homeassistant.const import CONF_NAME
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.trigger import PluggableAction
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .coordinator import WiiUCoordinator
from .triggers.turn_on import async_get_turn_on_trigger

LOGGER = logging.getLogger(__name__)

class WiiUEntity(CoordinatorEntity[WiiUCoordinator]):
    """Base entity for a Wii U device."""

    def __init__(self, coordinator: WiiUCoordinator) -> None:
        """Initialize entity and coordinator."""
        super().__init__(coordinator=coordinator)
        self._turn_on_action = PluggableAction(self.async_write_ha_state)

    @property
    def unique_id(self) -> str:
        """Generate a unique ID for this entity."""
        if self.entity_description is not None:
            return f"{self.coordinator.serial}_{self.entity_description.key}"
        return f"{self.coordinator.serial}_{self.name}"

    @property
    def device_info(self) -> DeviceInfo:
        """Return device info."""
        return DeviceInfo(
            identifiers={("nintendo_wiiu_ristretto", self.coordinator.serial)},
            manufacturer="Nintendo",
            name=self.coordinator.config_entry.data[CONF_NAME],
            hw_version=str(self.coordinator.hw_version),
            model=self.coordinator.model,
            serial_number=self.coordinator.serial,
            sw_version=self.coordinator.sw_version,
        )

    async def async_added_to_hass(self) -> None:
        """Add device triggers."""
        await super().async_added_to_hass()
        if (entry := self.registry_entry) and entry.device_id:
            self.async_on_remove(
                self._turn_on_action.async_register(
                    self.hass, async_get_turn_on_trigger(entry.device_id)
                )
            )
