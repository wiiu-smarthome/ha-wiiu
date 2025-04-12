"""Button platform for Wii U Ristretto."""

from collections.abc import Callable
from dataclasses import dataclass

from homeassistant.components.button import (
    ButtonDeviceClass,
    ButtonEntity,
    ButtonEntityDescription,
)
from homeassistant.const import EntityCategory

from .coordinator import WiiUCoordinator
from .entity import WiiUEntity


@dataclass(frozen=True, kw_only=True)
class WiiUButtonEntityDescription(ButtonEntityDescription):
    """Class describing Wii U button entities."""

    press_fn: Callable[[WiiUEntity], None] = lambda: None

ENTITY_DESCRIPTIONS: tuple[WiiUButtonEntityDescription, ...] = (
    WiiUButtonEntityDescription(
        key="restart",
        name="Restart",
        device_class=ButtonDeviceClass.RESTART,
        press_fn=lambda entity: entity.coordinator.async_reboot,
        icon="mdi:restart",
        entity_category=EntityCategory.DIAGNOSTIC
    ),
)

async def async_setup_entry(hass, config_entry, async_add_entities) -> None:
    """Set up the button platform."""
    coordinator = config_entry.runtime_data
    if not isinstance(coordinator, WiiUCoordinator):
        return
    for description in ENTITY_DESCRIPTIONS:
        async_add_entities([GenericWiiUButton(coordinator=coordinator, description=description)])


class GenericWiiUButton(WiiUEntity, ButtonEntity):
    """Representation of a Wii U button entity."""

    def __init__(
            self,
            coordinator: WiiUCoordinator,
            description: WiiUButtonEntityDescription
        ) -> None:
        """Initialize the button."""
        super().__init__(coordinator=coordinator)
        self.coordinator = coordinator
        self.entity_description: WiiUButtonEntityDescription = description

    async def async_press(self) -> None:
        """Perform a given action on press."""
        await self.entity_description.press_fn(self)
