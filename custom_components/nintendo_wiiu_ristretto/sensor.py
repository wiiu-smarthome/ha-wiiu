"""Sensors for Wii U."""

from collections.abc import Callable
from dataclasses import dataclass

from homeassistant.components.sensor import (
    RestoreSensor,
    SensorDeviceClass,
    SensorEntityDescription,
    SensorStateClass,
)

from .coordinator import WiiUCoordinator
from .entity import WiiUEntity


@dataclass(frozen=True, kw_only=True)
class WiiUSensorEntityDescription(SensorEntityDescription):
    """Class describing Wii U button entities."""

    value_fn: Callable[[WiiUEntity], None] = lambda: None


ENTITY_DESCRIPTIONS: list[WiiUSensorEntityDescription] = [
    WiiUSensorEntityDescription(
        key="gamepad_battery",
        native_unit_of_measurement="%",
        icon="mdi:battery",
        name="Gamepad Battery",
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.BATTERY,
        value_fn=lambda entity: entity.coordinator.gamepad_battery,
    )
]


async def async_setup_entry(hass, config_entry, async_add_entities) -> None:
    """Set up the button platform."""
    coordinator = config_entry.runtime_data
    if not isinstance(coordinator, WiiUCoordinator):
        return
    async_add_entities(
        [
            GenericWiiUSensor(coordinator=coordinator, description=description)
            for description in ENTITY_DESCRIPTIONS
        ]
    )


class GenericWiiUSensor(WiiUEntity, RestoreSensor):
    """Generic sensor for Wii U using a restore sensor."""

    def __init__(
        self, coordinator: WiiUCoordinator, description: WiiUSensorEntityDescription
    ) -> None:
        """Initialize the button."""
        super().__init__(coordinator=coordinator)
        self.coordinator = coordinator
        self.entity_description: WiiUSensorEntityDescription = description

    @property
    def native_value(self) -> int:
        """Return native value of the sensor."""
        return self.entity_description.value_fn(self)
