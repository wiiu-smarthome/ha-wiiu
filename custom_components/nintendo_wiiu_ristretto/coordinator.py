"""Update coordination."""

import json
import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_IP_ADDRESS, CONF_PORT, CONF_SCAN_INTERVAL
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from python_wiiu_ristretto import WiiU

_LOGGER = logging.getLogger(__name__)


class WiiUCoordinator(DataUpdateCoordinator):
    """Coordinate communication with Wii U."""

    serial: str = None
    source_list: list = None
    source: str = None
    model: str = None
    hw_version: str = None
    sw_version: str = None
    wii: WiiU = None
    title_map: dict = None

    def __init__(self, hass: HomeAssistant, config_entry: ConfigEntry) -> None:
        """Init."""
        super().__init__(
            hass,
            _LOGGER,
            name="Wii U Coordinator",
            config_entry=config_entry,
            update_interval=timedelta(
                seconds=config_entry.data.get(CONF_SCAN_INTERVAL, 10)
            ),
            always_update=True,
        )
        self.config_entry = config_entry
        self._ip_address = config_entry.data[CONF_IP_ADDRESS]
        self._ristretto_port = config_entry.data[CONF_PORT]
        self.is_on = False

    async def async_get_hardware_information(self) -> None:
        """Get hardware information."""
        self.serial = await self.hass.async_add_executor_job(
            self.wii.get_device_serial_id
        )
        self.hw_version = await self.hass.async_add_executor_job(
            self.wii.get_device_hardware_version
        )
        self.model = await self.hass.async_add_executor_job(
            self.wii.get_device_model_number
        )
        self.sw_version = await self.hass.async_add_executor_job(
            self.wii.get_device_version
        )

    def _get_current_app_name(self) -> None:
        """Get the current app name."""
        self.source = self.wii.get_current_title_name()

    def _get_source_list(self) -> None:
        """Get the source list."""
        self.title_map = json.loads(self.wii.get_title_list())
        self.source_list = []
        for value in self.title_map.values():
            self.source_list.append(value)

    def _launch_title(self, source: int) -> None:
        """Launch a given title on the Wii U."""
        self.wii.launch_title(source)

    async def _async_setup(self):
        """Set up the Wii U connection."""
        self.wii = WiiU(
            ip_address=self._ip_address, ristretto_port=self._ristretto_port
        )
        self.wii.timeout = self.config_entry.data.get(CONF_SCAN_INTERVAL)
        await self.async_get_hardware_information()
        await self.hass.async_add_executor_job(self._get_source_list)

    async def _async_update_data(self):
        """Update the data from the Wii U."""
        try:
            await self.hass.async_add_executor_job(self._get_current_app_name)
            await self.hass.async_add_executor_job(self._get_source_list)
            self.is_on = True
        except Exception as e:
            self.is_on = False

    async def async_reboot(self) -> None:
        await self.hass.async_add_executor_job(self.wii.reboot)
