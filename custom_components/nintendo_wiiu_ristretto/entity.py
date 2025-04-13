"""Base entity for a Wii U device."""

from homeassistant.const import CONF_NAME
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from custom_components.nintendo_wiiu_ristretto.coordinator import WiiUCoordinator


class WiiUEntity(CoordinatorEntity[WiiUCoordinator]):
    """Base entity for a Wii U device."""

    def __init__(self, coordinator: WiiUCoordinator) -> None:
        """Initialize entity and coordinator."""
        super().__init__(coordinator=coordinator)
        self._attr_unique_id = coordinator.config_entry.entry_id

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
