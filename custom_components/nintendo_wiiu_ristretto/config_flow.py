"""Config flow handling."""

from typing import Any

import voluptuous as vol

from homeassistant.const import CONF_IP_ADDRESS, CONF_PORT, CONF_NAME
from homeassistant.config_entries import ConfigFlow, ConfigFlowResult

from .const import DOMAIN

SCHEMA = vol.Schema(
    {
        vol.Required(CONF_IP_ADDRESS): str,
        vol.Required(CONF_PORT, default=8572): int,
        vol.Optional(CONF_NAME, default="Wii U"): str,
    }
)

class ConfigFlowHandler(ConfigFlow, domain=DOMAIN):
    """Handle flow."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """User setup step."""
        errors = {}
        if user_input is not None:
            return self.async_create_entry(title=user_input[CONF_NAME], data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=SCHEMA,
            errors=errors,
        )
