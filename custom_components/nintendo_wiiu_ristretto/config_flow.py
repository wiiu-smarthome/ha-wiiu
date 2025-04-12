"""Config flow handling."""

from typing import Any

import voluptuous as vol
from homeassistant.config_entries import ConfigFlow, ConfigFlowResult

from custom_components.nintendo_wiiu_ristretto import DOMAIN


class ConfigFlowHandler(ConfigFlow, domain=DOMAIN):
    """Handle flow."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """User setup step."""
        errors = {}
        if user_input is not None:
            return self.async_create_entry(title="Wii U", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({"ip": str, "port": int}),
            errors=errors,
        )
