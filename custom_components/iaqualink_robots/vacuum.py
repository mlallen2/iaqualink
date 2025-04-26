from homeassistant.components.vacuum import StateVacuumEntity, VacuumEntityFeature, VacuumActivity
from homeassistant.helpers.entity import DeviceInfo
from .const import DOMAIN, SUPPORT_FLAGS
from .coordinator import IAquaLinkCoordinator

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up vacuum from a config entry."""
    coordinator: IAquaLinkCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([IAquaLinkRobotVacuum(coordinator, entry)])

class IAquaLinkRobotVacuum(StateVacuumEntity):
    def __init__(self, coordinator, entry):
        super().__init__()
        self.coordinator = coordinator
        self._attr_name = entry.title
        self._attr_supported_features = SUPPORT_FLAGS
        self._attr_unique_id = coordinator.data["device"]["serial_number"]
        self._fan_speed_list = ["Floor only","Floor and walls","SMART"]

    @property
    def device_info(self):
        return DeviceInfo(
            identifiers={(DOMAIN, self._attr_unique_id)},
            name=self._attr_name,
            manufacturer="iAqualink",
            model=self.coordinator.data["features"].get("model"),
        )

    @property
    def activity(self) -> VacuumActivity:
        return VacuumActivity.CLEANING if self.coordinator.data["status"]["status"] == "connected" else VacuumActivity.IDLE

    @property
    def fan_speed_list(self):
        return self._fan_speed_list

    async def async_start(self):
        # call API via coordinator.data and schedule refresh
        await self.coordinator.async_request_refresh()

    async def async_stop(self, **kwargs):
        await self.coordinator.async_request_refresh()

    async def async_update(self):
        # HA will not call this; coordinator drives updates
        pass

    @property
    def extra_state_attributes(self):
        return self.coordinator.data["status"]
