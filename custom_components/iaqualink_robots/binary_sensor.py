from homeassistant.components.binary_sensor import BinarySensorEntity
from .const import DOMAIN
from .coordinator import IAquaLinkCoordinator

async def async_setup_entry(hass, entry, async_add_entities):
    coord: IAquaLinkCoordinator = hass.data[DOMAIN][entry.entry_id]
    vacuum = IAquaLinkRobotVacuum(coord, entry)
    async_add_entities([
        IAquaLinkBinarySensor(vacuum, "canister", lambda v: v > 0, "Canister Full"),
        IAquaLinkBinarySensor(vacuum, "error_state", lambda v: v != 0, "Error State"),
        IAquaLinkBinarySensor(vacuum, None, lambda v: v == "connected", "Cleaning Active", source="status")
    ])

class IAquaLinkBinarySensor(BinarySensorEntity):
    def __init__(self, vac, key, fn, label, source="status"):
        self.vac = vac
        self.key = key
        self.fn = fn
        self._attr_name = f"{vac.name} {label}"
        self.source = source

    @property
    def is_on(self):
        val = self.vac.coordinator.data[self.source].get(self.key)
        return bool(self.fn(val))

    @property
    def available(self):
        return True

    @property
    def device_info(self):
        return self.vac.device_info

    async def async_update(self):
        await self.vac.coordinator.async_request_refresh()

