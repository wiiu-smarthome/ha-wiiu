"""Represent a media player entity for the Nintendo Wii U console."""

from homeassistant.components.media_player import (
    MediaPlayerDeviceClass,
    MediaPlayerEntity,
)
from homeassistant.components.media_player.const import (
    MediaPlayerEntityFeature,
    MediaPlayerState,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from custom_components.nintendo_wiiu_ristretto.coordinator import WiiUCoordinator
from custom_components.nintendo_wiiu_ristretto.entity import WiiUEntity


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Wii U media player entity."""
    # TODO: Make list, handle devices being offline
    async_add_entities(
        [
            NintendoWiiUMediaPlayer(
                coordinator=config_entry.runtime_data, name=config_entry.data[CONF_NAME]
            )
        ]
    )


class NintendoWiiUMediaPlayer(WiiUEntity, MediaPlayerEntity):
    """Representation of a Wii U console."""

    _attr_icon = "mdi:nintendo-wiiu"
    _attr_supported_features = (
        MediaPlayerEntityFeature.TURN_OFF | MediaPlayerEntityFeature.SELECT_SOURCE
    )

    def __init__(self, coordinator: WiiUCoordinator, name: str):
        """Initialize the Wii U media player entity."""
        super().__init__(coordinator=coordinator)
        self.coordinator = coordinator
        self._attr_name = name
        self._attr_device_class = MediaPlayerDeviceClass.TV
        self._attr_source = coordinator.source
        self._attr_source_list = coordinator.source_list

    @property
    def app_name(self) -> str:
        """Return the name of the currently running app."""
        return self.coordinator.source

    @property
    def source(self) -> str:
        """Return the name of the source (the currently running app)."""
        return self.coordinator.source

    @property
    def state(self) -> MediaPlayerState:
        """Return the state of the device."""
        if self.coordinator.is_on:
            return MediaPlayerState.ON
        return MediaPlayerState.OFF

    async def async_select_source(self, source: str) -> None:
        """Select a source on the Wii U console."""
        for titleid, name in self.coordinator.title_map.items():
            if name == source:
                return await self.hass.async_add_executor_job(
                    self.coordinator.wii.launch_title, titleid
                )
        return None

    async def async_turn_off(self) -> None:
        """Turn off the Wii U console."""
        await self.hass.async_add_executor_job(self.coordinator.wii.shutdown)
