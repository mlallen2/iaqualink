import asyncio
from homeassistant.components.binary_sensor import BinarySensorEntity
from .const import DOMAIN
from .coordinator import IAquaLinkCoordinator
from .vacuum import IAquaLinkRobotVacuum

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the binary sensors for iAqualink Robots."""
    coord: IAquaLinkCoordinator = hass.data[DOMAIN][entry.entry_id]
    vacuum = IAquaLinkRobotVacuum(coord, entry)
    async_add_entities([
        IAquaLinkBinarySensor(vacuum, "canister", lambda v: v > 0, "Canister Full"),
        IAquaLinkBinarySensor(vacuum, "error_state", lambda v: v != 0, "Error State"),
        IAquaLinkBinarySensor(vacuum, None, lambda v: v == "connected", "Cleaning Active", source="status")
    ])

class IAquaLinkBinarySensor(BinarySensorEntity):
    """Generic binary sensor for iAqualink Robot attributes."""

    def __init__(self, vac: IAquaLinkRobotVacuum, key: str, fn, label: str, source: str = "status"):
        self.vac = vac
        self.key = key
        self.fn = fn
        self._attr_name = f"{vac.name} {label}"
        self.source = source

    @property
    def is_on(self) -> bool:
        val = self.vac.coordinator.data[self.source].get(self.key)
        return bool(self.fn(val))

    @property
    def available(self) -> bool:
        return True

    @property
    def device_info(self):
        return self.vac.device_info

    async def async_update(self):
        await self.vac.coordinator.async_request_refresh()
