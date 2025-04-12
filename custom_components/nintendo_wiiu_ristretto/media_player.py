from homeassistant.components.media_player import (
    MediaPlayerDeviceClass,
    MediaPlayerEntity,
)
from homeassistant.components.media_player.const import (
    MediaPlayerEntityFeature,
    MediaPlayerState,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from custom_components.nintendo_wiiu_ristretto.coordinator import WiiUCoordinator
from custom_components.nintendo_wiiu_ristretto.entity import WiiUEntity


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    # TODO: Make list, handle devices being offline
    async_add_entities([NintendoWiiUMediaPlayer(coordinator=config_entry.runtime_data)])


class NintendoWiiUMediaPlayer(WiiUEntity, MediaPlayerEntity):
    """Representation of a Wii U console."""

    _attr_icon = "mdi:nintendo-wiiu"
    _attr_supported_features = (
        MediaPlayerEntityFeature.TURN_OFF | MediaPlayerEntityFeature.SELECT_SOURCE
    )

    def __init__(self, coordinator: WiiUCoordinator):
        super().__init__(coordinator=coordinator)
        self.coordinator = coordinator
        self._attr_name = "Wii U"
        self._attr_device_class = MediaPlayerDeviceClass.TV
        self._attr_source = coordinator.source
        self._attr_source_list = coordinator.source_list

    @property
    def app_name(self) -> str:
        return self.coordinator.source

    @property
    def state(self) -> MediaPlayerState:
        if self.coordinator.is_on:
            return MediaPlayerState.ON
        return MediaPlayerState.OFF

    @property
    def device_info(self) -> DeviceInfo:
        return self.coordinator._attr_device_info

    @property
    def unique_id(self) -> str:
        return self.coordinator.serial

    async def async_get_device_info(self):
        await self.coordinator.async_get_device_info()

    async def async_select_source(self, source: str) -> None:
        await self.coordinator.async_select_source(source)

    async def async_update(self) -> None:
        return await self.coordinator._async_update_data()

    async def async_turn_off(self):
        await self.coordinator.async_turn_off()
