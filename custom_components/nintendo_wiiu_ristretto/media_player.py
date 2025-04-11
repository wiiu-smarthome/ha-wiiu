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
from python_wiiu_ristretto import WiiU

from custom_components.nintendo_wiiu_ristretto import DOMAIN


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    # TODO: Make list, handle devices being offline
    config = config_entry
    async_add_entities(
        [
            NintendoWiiUConsole(
                config=config_entry,
                ip=config_entry.data["ip"],
                ristretto_port=config_entry.data["port"],
            )
        ],
        update_before_add=True,
    )


class NintendoWiiUConsole(MediaPlayerEntity):
    """Representation of a Wii U console."""

    _attr_icon = "mdi:nintendo-wiiu"
    _attr_supported_features = (
        MediaPlayerEntityFeature.TURN_OFF | MediaPlayerEntityFeature.SELECT_SOURCE
    )

    _title_map = dict

    def __init__(self, config: ConfigEntry, ip: str, ristretto_port: int) -> None:
        self.name = "Wii U"
        self.config = config
        self._attr_unique_id = config.entry_id
        self._attr_device_class = MediaPlayerDeviceClass.TV
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self.config.entry_id)},
            manufacturer="Nintendo",
            name="Wii U",
        )
        self.source_list = []
        self._wiiu = WiiU(ip_address=ip, ristretto_port=ristretto_port)

    def _get_device_info(self) -> None:
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self.config.entry_id)},
            manufacturer="Nintendo",
            hw_version=str(self._wiiu.get_device_hardware_version()),
            model=self._wiiu.get_device_model_number(),
            serial_number=self._wiiu.get_device_serial_id(),
            sw_version=self._wiiu.get_device_version(),
        )

    def _get_current_app_name(self) -> None:
        self.source = self._wiiu.get_current_title_name()
        self.app_name = self.source
        self.state = MediaPlayerState.ON

    def _get_source_list(self) -> None:
        self._title_map = self._wiiu.get_title_list()
        self.source_list = []
        for value in self._title_map.values():
            self.source_list.append(value)

    def _launch_title(self, source: int) -> None:
        self._wiiu.launch_title(source)

    async def async_update(self) -> None:
        # TODO: Handle console being off
        if self._attr_device_info is None:
            await self.hass.async_add_executor_job(self._get_device_info)
        if self.source_list == []:
            await self.hass.async_add_executor_job(self._get_source_list)
        await self.hass.async_add_executor_job(self._get_current_app_name)

    async def async_select_source(self, source: str) -> None:
        # Unlike Homebridge, the ID of the source actually is more important so we need to search for it
        for titleid, name in self._title_map.items():
            if name == source:
                return await self.hass.async_add_executor_job(
                    self._launch_title, titleid
                )
        return None

    async def async_turn_off(self) -> None:
        await self.hass.async_add_executor_job(self._wiiu.shutdown)
