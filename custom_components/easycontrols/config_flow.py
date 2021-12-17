import eazyctrl

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_NAME
from .const import CONTROLLER, DOMAIN, VARIABLE_ARTICLE_DESCRIPTION, VARIABLE_MAC_ADDRESS, MAC_ADDRESS


@config_entries.HANDLERS.register(DOMAIN)
class EasyControlsConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, info):
        data_schema = vol.Schema({
            vol.Required(CONF_HOST): str,
            vol.Required(CONF_NAME): str
        })
        
        if info is not None:
            await self.async_set_unique_id(info[CONF_NAME])
            self._abort_if_unique_id_configured()

            try:
                controller = eazyctrl.EazyController(info[CONF_HOST])
                device_type = controller.get_variable(VARIABLE_ARTICLE_DESCRIPTION, 31)
                mac_address = controller.get_variable(VARIABLE_MAC_ADDRESS, 18, str)
            except:
                 return self.async_show_form(
                    step_id="user",
                    data_schema=data_schema,
                    errors={CONF_HOST: "invalid_host"}
                )

            data = {CONF_NAME: info[CONF_NAME],
                    CONF_HOST: info[CONF_HOST], MAC_ADDRESS: mac_address}
            
            return self.async_create_entry(
                title=f"Helios {device_type} ({info[CONF_NAME]})", data=data
            )

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
        )
