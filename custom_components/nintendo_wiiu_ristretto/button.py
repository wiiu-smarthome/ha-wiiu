from custom_components.nintendo_wiiu_ristretto import coordinator
from custom_components.nintendo_wiiu_ristretto.coordinator import WiiUCoordinator
from custom_components.nintendo_wiiu_ristretto.entity import WiiUEntity

from homeassistant.components.button import (
    ButtonDeviceClass,
    ButtonEntity,
    ButtonEntityDescription,
)


async def async_setup_entry(hass, config_entry, async_add_entities) -> None:
    async_add_entities([RestartButton(coordinator=config_entry.runtime_data)])


class RestartButton(WiiUEntity, ButtonEntity):
    def __init__(self, coordinator: WiiUCoordinator) -> None:
        """Initialize the button."""
        super().__init__(coordinator=coordinator)
        self.coordinator = coordinator
        self.name = "Restart Wii U"

    async def async_press(self) -> None:
        """Restart console."""
        await self.coordinator.async_reboot()
