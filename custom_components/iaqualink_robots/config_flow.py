import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from .const import DOMAIN, URL_LOGIN

STEP_USER_DATA_SCHEMA = vol.Schema({
    vol.Required("username"): str,
    vol.Required("password"): str,
    vol.Required("api_key"):   str,
    vol.Optional("name", default="Pool Robot"): str,
})

class IaqualinkConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for iAqualink Robots."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    async def async_step_user(self, user_input=None):
        """Initial step: ask for credentials."""
        errors = {}
        if user_input is not None:
            session = self.hass.helpers.aiohttp_client.async_get_clientsession()
            try:
                resp = await session.post(
                    URL_LOGIN,
                    json={
                        "apikey":  user_input["api_key"],
                        "email":   user_input["username"],
                        "password":user_input["password"],
                    },
                    timeout=10
                )
                resp.raise_for_status()
                auth = await resp.json()
                if "authentication_token" not in auth:
                    raise ValueError("no_token")
            except Exception:
                errors["base"] = "auth"
            else:
                return self.async_create_entry(
                    title=user_input["name"],
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """No options for now."""
        return None
