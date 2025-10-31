"""Config flow handling."""

from typing import Any

import voluptuous as vol
from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.const import (
    ATTR_HW_VERSION,
    ATTR_MODEL,
    ATTR_SERIAL_NUMBER,
    ATTR_SW_VERSION,
    CONF_IP_ADDRESS,
    CONF_NAME,
    CONF_PORT,
    CONF_SCAN_INTERVAL,
    CONF_TIMEOUT,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from python_wiiu_ristretto import WiiU

from .const import DEFAULT_TIMEOUT, DOMAIN

SCHEMA = vol.Schema(
    {
        vol.Required(CONF_IP_ADDRESS): str,
        vol.Required(CONF_PORT, default=8572): int,
        vol.Optional(CONF_NAME, default="Wii U"): str,
        vol.Optional(CONF_SCAN_INTERVAL, default=10): int,
        vol.Optional(CONF_TIMEOUT, default=DEFAULT_TIMEOUT): int,
    }
)


async def get_device_info(
    hass: HomeAssistant,
    ip_addres: str,
    port: int,
    timeout: int  # noqa: ASYNC109
) -> tuple[str, str, str, str]:
    """Return device info from Wii U."""
    wii = WiiU(
        ip_address=ip_addres,
        ristretto_port=port,
        session=async_get_clientsession(hass),
        timeout=timeout,
    )
    serial = await wii.async_get_device_serial_id()
    hw_version = str(await wii.async_get_device_hardware_version())
    model = await wii.async_get_device_model_number()
    sw_version = await wii.async_get_device_version()
    return serial, hw_version, model, sw_version


class WiiUConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle flow."""

    VERSION = 2

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """User setup step."""
        errors = {}
        if user_input is not None:
            await self.async_set_unique_id(f"{DOMAIN}_{user_input[CONF_IP_ADDRESS]}")
            self._abort_if_unique_id_configured()
            try:
                serial, hw_version, model, sw_version = await get_device_info(
                    hass=self.hass,
                    ip_addres=user_input[CONF_IP_ADDRESS],
                    port=user_input[CONF_PORT],
                    timeout=user_input[CONF_TIMEOUT],
                )
            except (TimeoutError, ConnectionError):
                errors["base"] = "cannot_connect"
            else:
                user_input = {
                    **user_input,
                    ATTR_SERIAL_NUMBER: serial,
                    ATTR_HW_VERSION: hw_version,
                    ATTR_MODEL: model,
                    ATTR_SW_VERSION: sw_version,
                }
                return self.async_create_entry(
                    title=user_input[CONF_NAME], data=user_input
                )
        return self.async_show_form(
            step_id="user",
            data_schema=SCHEMA,
            errors=errors,
        )
