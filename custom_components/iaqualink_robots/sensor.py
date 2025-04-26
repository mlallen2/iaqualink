from homeassistant.components.sensor import SensorEntity
from .const import DOMAIN
from .coordinator import IAquaLinkCoordinator

async def async_setup_entry(hass, entry, async_add_entities):
    coord: IAquaLinkCoordinator = hass.data[DOMAIN][entry.entry_id]
    vacuum = IAquaLinkRobotVacuum(coord, entry)
    sensors = []
    data = coord.data["status"]
    for key in ("temperature","canister","error_state","total_hours","cycle","cycle_duration","cycle_end_time","time_remaining","last_online"):
        sensors.append(IAquaLinkStatusSensor(vacuum, key))
    async_add_entities(sensors)

class IAquaLinkStatusSensor(SensorEntity):
    def __init__(self, vac_entity, key):
        self.vac = vac_entity
        self.key = key
        self._attr_name = f"{vac_entity.name} {key.replace('_',' ').title()}"

    @property
    def state(self):
        return self.vac.coordinator.data["status"].get(self.key)

    @property
    def available(self):
        return True

    @property
    def device_info(self):
        return self.vac.device_info

    async def async_update(self):
        await self.vac.coordinator.async_request_refresh()

