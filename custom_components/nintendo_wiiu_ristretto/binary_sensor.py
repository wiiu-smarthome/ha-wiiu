"""Binary sensor components for Ristretto."""

from collections.abc import Callable
from dataclasses import dataclass

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .coordinator import WiiUCoordinator
from .entity import WiiUEntity


@dataclass(frozen=True, kw_only=True)
class WiiUBinarySensorEntityDescription(BinarySensorEntityDescription):
    """Class describing Wii U binary sensor entities."""

    is_on_fn: Callable[[WiiUEntity], None] = lambda: None


ENTITY_DESCRIPTIONS = [
    WiiUBinarySensorEntityDescription(
        key="gamepad_charging",
        device_class=BinarySensorDeviceClass.BATTERY_CHARGING,
        name="Gamepad Charging",
        is_on_fn=lambda entity: entity.coordinator.gamepad_charging,
    )
]


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001
    config_entry: ConfigEntry,
    async_add_entities: Callable[[list[BinarySensorEntity]], None],
) -> None:
    """Set up the button platform."""
    coordinator = config_entry.runtime_data
    if not isinstance(coordinator, WiiUCoordinator):
        return
    async_add_entities(
        [
            GenericWiiUBinarySensor(coordinator=coordinator, description=description)
            for description in ENTITY_DESCRIPTIONS
        ]
    )


class GenericWiiUBinarySensor(WiiUEntity, BinarySensorEntity):
    """A generic Wii U binary sensor."""

    def __init__(
        self,
        coordinator: WiiUCoordinator,
        description: WiiUBinarySensorEntityDescription,
    ) -> None:
        """Initialize a binary sensor."""
        super().__init__(coordinator)
        self.coordinator = coordinator
        self.entity_description: WiiUBinarySensorEntityDescription = description

    @property
    def is_on(self) -> bool:
        """Return true if the binary sensor is on."""
        return self.entity_description.is_on_fn(self)
