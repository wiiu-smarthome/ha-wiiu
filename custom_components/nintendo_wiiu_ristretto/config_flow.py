"""Config flow handling."""

from typing import Any

import voluptuous as vol
from homeassistant.components.media_player import DOMAIN as MP_DOMAIN
from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.const import (
    CONF_IP_ADDRESS,
    CONF_NAME,
    CONF_PORT,
    CONF_SCAN_INTERVAL,
    CONF_TIMEOUT,
)
from homeassistant.data_entry_flow import AbortFlow
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.service_info.dhcp import DhcpServiceInfo

from .const import DEFAULT_TIMEOUT, DEFAULT_UPDATE_INTERVAL, DOMAIN

SCHEMA = vol.Schema(
    {
        vol.Required(CONF_IP_ADDRESS): str,
        vol.Required(CONF_PORT, default=8572): int,
        vol.Optional(CONF_NAME, default="Wii U"): str,
        vol.Optional(CONF_SCAN_INTERVAL, default=DEFAULT_UPDATE_INTERVAL): int,
        vol.Optional(CONF_TIMEOUT, default=DEFAULT_TIMEOUT): int,
    }
)


class ConfigFlowHandler(ConfigFlow, domain=DOMAIN):
    """Handle flow."""

    VERSION = 2
    _dhcp_discovery_info = None

    async def async_step_dhcp(self, discovery_info: DhcpServiceInfo) -> ConfigFlowResult:
        """Process initial DHCP discovery step."""
        self._dhcp_discovery_info = discovery_info
        await self.async_set_unique_id(discovery_info.ip)
        self._abort_if_unique_id_configured()
        registry = er.async_get(self.hass)

        if registry.async_get_entity_id(
            MP_DOMAIN, DOMAIN, discovery_info.ip
        ) is not None:
            raise AbortFlow("already_configured")
        return await self.async_step_dhcp_confirm()

    async def async_step_dhcp_confirm(
            self,
            user_input: dict[str, Any] | None = None
        ) -> ConfigFlowResult:
        """DHCP Discovery configuration."""
        if user_input is not None:
            return self.async_create_entry(title=user_input[CONF_NAME], data=user_input)
        configuration = {
            CONF_IP_ADDRESS: self._dhcp_discovery_info.ip,
            CONF_PORT: 8572,
            CONF_TIMEOUT: DEFAULT_TIMEOUT,
            CONF_SCAN_INTERVAL: DEFAULT_UPDATE_INTERVAL
        }
        return self.async_show_form(
            step_id="dhcp_confirm",
            data_schema=self.add_suggested_values_to_schema(
                data_schema=SCHEMA,
                suggested_values=configuration
            ),
            description_placeholders={
                CONF_IP_ADDRESS: self._dhcp_discovery_info.ip
            }
        )

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """User setup step."""
        errors = {}
        if user_input is not None:
            await self.async_set_unique_id(user_input[CONF_IP_ADDRESS])
            self._abort_if_unique_id_configured()
            return self.async_create_entry(title=user_input[CONF_NAME], data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=SCHEMA,
            errors=errors,
        )
