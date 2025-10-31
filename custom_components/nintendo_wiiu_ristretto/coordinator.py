"""Update coordination."""

import json
import logging
from datetime import timedelta

from aiohttp import ClientOSError
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    CONF_IP_ADDRESS,
    CONF_PORT,
    CONF_SCAN_INTERVAL,
    CONF_TIMEOUT,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from python_wiiu_ristretto import WiiU

from .const import DEFAULT_TIMEOUT, DEFAULT_UPDATE_INTERVAL

_LOGGER = logging.getLogger(__name__)


class WiiUCoordinator(DataUpdateCoordinator):
    """Coordinate communication with Wii U."""

    gamepad_charging: bool = False
    gamepad_battery: int = None
    source_list: list = None
    source: str = None
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
                seconds=config_entry.data.get(
                    CONF_SCAN_INTERVAL, DEFAULT_UPDATE_INTERVAL
                )
            ),
            always_update=True,
        )
        self.config_entry = config_entry
        self._ip_address = config_entry.data[CONF_IP_ADDRESS]
        self._ristretto_port = config_entry.data[CONF_PORT]
        self.is_on = False

    async def _get_current_app_name(self) -> None:
        """Get the current app name."""
        self.source = await self.wii.async_get_current_title_name()

    async def _get_source_list(self) -> None:
        """Get the source list."""
        self.title_map = json.loads(await self.wii.async_get_title_list())
        self.source_list = list(self.title_map.values())

    async def _async_setup(self) -> None:
        """Set up the Wii U connection."""
        self.wii = WiiU(
            ip_address=self._ip_address,
            ristretto_port=self._ristretto_port,
            session=async_get_clientsession(self.hass),
            timeout=self.config_entry.data.get(CONF_TIMEOUT, DEFAULT_TIMEOUT),
        )

    async def _async_update_data(self) -> None:
        """Update the data from the Wii U."""
        try:
            if self.title_map is None:
                await self._get_source_list()
            await self._get_current_app_name()
            self.gamepad_battery = await self.wii.async_get_gamepad_battery()
            if isinstance(self.gamepad_battery, int):
                if self.gamepad_battery == 0:
                    # battery charging
                    self.gamepad_charging = True
                    self.gamepad_battery = 100
                else:
                    self.gamepad_charging = False
                    self.gamepad_battery = ((self.gamepad_battery - 1) / 5) * 100
            self.is_on = True
        except ClientOSError:
            # discard connection errors
            pass
        except (TimeoutError, ConnectionError):
            self.is_on = False
        except Exception as e:
            _LOGGER.exception("Error updating data", exc_info=e)
            return False
        return True
