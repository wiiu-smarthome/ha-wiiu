"""Base entity for a Wii U device."""

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from custom_components.nintendo_wiiu_ristretto.coordinator import WiiUCoordinator


class WiiUEntity(CoordinatorEntity[WiiUCoordinator]):
    """Base entity for a Wii U device."""

    def __init__(self, coordinator: WiiUCoordinator) -> None:
        """Initialize entity and coordinator."""
        super().__init__(coordinator=coordinator)
        self._attr_unique_id = coordinator.config_entry.entry_id

        self._attr_device_info = DeviceInfo(
            identifiers={("nintendo_wiiu_ristretto", coordinator.serial)},
            manufacturer="Nintendo",
            name="Wii U",
        )
