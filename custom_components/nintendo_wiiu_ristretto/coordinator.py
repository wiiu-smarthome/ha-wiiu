"""Update coordination."""

import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from python_wiiu_ristretto import WiiU

_LOGGER = logging.getLogger(__name__)


class WiiUCoordinator(DataUpdateCoordinator):
    """Coordinate communication with Wii U."""

    def __init__(
        self,
        hass: HomeAssistant,
        config_entry: ConfigEntry,
        ip_address: str,
        ristretto_port: int,
    ):
        """Init."""
        super().__init__(
            hass,
            _LOGGER,
            name="Wii U Coordinator",
            config_entry=config_entry,
            update_interval=timedelta(10),
            always_update=True,
        )
        self.config_entry = config_entry
        self._ip_address = ip_address
        self._ristretto_port = ristretto_port
        self._wiiu = None
        self.is_on = False
        self._title_map = dict

    def _get_current_app_name(self) -> None:
        self.source = self._wiiu.get_current_title_name()

    def _get_device_info(self) -> None:
        # TODO: maybe dont hardcode name
        self._attr_device_info = DeviceInfo(
            identifiers={("nintendo_wiiu_ristretto", self.serial)},
            manufacturer="Nintendo",
            name="Wii U",
            hw_version=str(self._wiiu.get_device_hardware_version()),
            model=self._wiiu.get_device_model_number(),
            serial_number=self.serial,
            sw_version=self._wiiu.get_device_version(),
        )

    def _get_serial(self) -> None:
        self.serial = self._wiiu.get_device_serial_id()
        self.unique_id = self.serial

    def _get_source_list(self) -> None:
        self._title_map = self._wiiu.get_title_list()
        self.source_list = []
        for value in self._title_map.values():
            self.source_list.append(value)

    def _launch_title(self, source: int) -> None:
        self._wiiu.launch_title(source)

    async def async_get_device_info(self) -> None:
        await self.hass.async_add_executor_job(self._get_device_info)

    async def _async_setup(self):
        self._wiiu = WiiU(
            ip_address=self._ip_address, ristretto_port=self._ristretto_port
        )
        await self.hass.async_add_executor_job(self._get_serial)
        await self.hass.async_add_executor_job(self._get_device_info)
        await self.hass.async_add_executor_job(self._get_source_list)

    async def _async_update_data(self):
        try:
            await self.hass.async_add_executor_job(self._get_current_app_name)
            self.is_on = True
        except:
            self.is_on = False

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
        self.is_on = False

    async def async_reboot(self) -> None:
        await self.hass.async_add_executor_job(self._wiiu.reboot)
