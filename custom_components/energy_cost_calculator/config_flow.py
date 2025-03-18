"""Adds config flow for Energy Cost Calculator."""
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers.aiohttp_client import async_create_clientsession

from .api import EnergyCostCalculatorApiClient
from .const import CONF_PASSWORD
from .const import CONF_USERNAME
from .const import DOMAIN
from .const import PLATFORMS


class EnergyCostCalculatorFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for energy_cost_calculator."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            return self.async_create_entry(title=user_input["name"], data=user_input)

        data_schema = vol.Schema(
            {
                vol.Required("name"): str,
                vol.Required("energy_sensor"): selector({"entity": {"domain": "sensor"}}),
                vol.Optional("cost_sensor"): selector({"entity": {"domain": "sensor"}}),
                vol.Optional("gas_sensor"): selector({"entity": {"domain": "sensor"}}),
            }
        )

        return self.async_show_form(step_id="user", data_schema=data_schema, errors=errors)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return EnergyOptionsFlowHandler(config_entry)


class EnergyCostCalculatorOptionsFlowHandler(config_entries.OptionsFlow):
    """Config flow options handler for energy_cost_calculator."""

    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage options for the integration."""
        errors = {}

        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        data_schema = vol.Schema(
            {
                vol.Optional("energy_sensor", default=self.config_entry.options.get("energy_sensor")): selector({"entity": {"domain": "sensor"}}),
                vol.Optional("cost_sensor", default=self.config_entry.options.get("cost_sensor")): selector({"entity": {"domain": "sensor"}}),
                vol.Optional("gas_sensor", default=self.config_entry.options.get("gas_sensor")): selector({"entity": {"domain": "sensor"}}),
            }
        )

        return self.async_show_form(step_id="init", data_schema=data_schema, errors=errors)

