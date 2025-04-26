import asyncio, json, datetime, aiohttp
from datetime import timedelta

from homeassistant.components.vacuum import (
    StateVacuumEntity,
    VacuumEntityFeature,
    VacuumActivity
)
from homeassistant.components.sensor import SensorEntity
from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.const import STATE_ON, STATE_OFF

from .const import (
    URL_LOGIN, URL_GET_DEVICES, URL_GET_DEVICE_STATUS,
    URL_GET_DEVICE_FEATURES, DOMAIN, SCAN_INTERVAL
)

SUPPORT_FLAGS = (
    VacuumEntityFeature.START
    | VacuumEntityFeature.STOP
    | VacuumEntityFeature.FAN_SPEED
    | VacuumEntityFeature.STATUS
    | VacuumEntityFeature.RETURN_HOME
)

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up iAqualink Custom vacuum + all attribute entities."""
    vacuum = IAquaLinkRobotVacuum(config)
    entities = [
        vacuum,
        IAquaLinkUsernameSensor(vacuum),
        IAquaLinkFirstNameSensor(vacuum),
        IAquaLinkLastNameSensor(vacuum),
        IAquaLinkIDSensor(vacuum),
        IAquaLinkSerialSensor(vacuum),
        IAquaLinkDeviceTypeSensor(vacuum),
        IAquaLinkLastOnlineSensor(vacuum),
        IAquaLinkTemperatureSensor(vacuum),
        IAquaLinkTotalHoursSensor(vacuum),
        IAquaLinkCycleStartSensor(vacuum),
        IAquaLinkCycleSensor(vacuum),
        IAquaLinkCycleDurationSensor(vacuum),
        IAquaLinkCycleEndSensor(vacuum),
        IAquaLinkTimeRemainingSensor(vacuum),
        IAquaLinkModelSensor(vacuum),
        IAquaLinkCanisterFullSensor(vacuum),
    ]
    async_add_entities(entities)

class IAquaLinkRobotVacuum(StateVacuumEntity):
    """Represents an iaqualink_robots vacuum."""

    def __init__(self, config):
        super().__init__()
        # Required so HA can pass your YAML
        self._name     = config.get("name")
        self._username = config.get("username")
        self._password = config.get("password")
        self._api_key  = config.get("api_key")

        # Basic state holders for your sensors
        self._attributes         = {}
        self._activity           = VacuumActivity.IDLE
        self._status             = STATE_OFF
        self._supported_features = SUPPORT_FLAGS
        self._temperature        = None
        self._battery_level      = None

    @property
    def supported_features(self):
        return self._supported_features

# ──────── SensorEntity classes ────────

class IAquaLinkUsernameSensor(SensorEntity):
    def __init__(self, vac):
        self._vac = vac
        self._attr_name = f"{vac.name} Username"
    @property
    def state(self):
        return self._vac._attributes.get("username")
    @property
    def available(self):
        return self._vac.available
    async def async_update(self):
        await self._vac.async_update()

class IAquaLinkFirstNameSensor(SensorEntity):
    def __init__(self, vac):
        self._vac = vac
        self._attr_name = f"{vac.name} First Name"
    @property
    def state(self):
        return self._vac._attributes.get("first_name")
    @property
    def available(self):
        return self._vac.available
    async def async_update(self):
        await self._vac.async_update()

class IAquaLinkLastNameSensor(SensorEntity):
    def __init__(self, vac):
        self._vac = vac
        self._attr_name = f"{vac.name} Last Name"
    @property
    def state(self):
        return self._vac._attributes.get("last_name")
    @property
    def available(self):
        return self._vac.available
    async def async_update(self):
        await self._vac.async_update()

class IAquaLinkIDSensor(SensorEntity):
    def __init__(self, vac):
        self._vac = vac
        self._attr_name = f"{vac.name} User ID"
    @property
    def state(self):
        return self._vac._attributes.get("id")
    @property
    def available(self):
        return self._vac.available
    async def async_update(self):
        await self._vac.async_update()

class IAquaLinkSerialSensor(SensorEntity):
    def __init__(self, vac):
        self._vac = vac
        self._attr_name = f"{vac.name} Serial Number"
    @property
    def state(self):
        return self._vac._attributes.get("serial_number")
    @property
    def available(self):
        return self._vac.available
    async def async_update(self):
        await self._vac.async_update()

class IAquaLinkDeviceTypeSensor(SensorEntity):
    def __init__(self, vac):
        self._vac = vac
        self._attr_name = f"{vac.name} Device Type"
    @property
    def state(self):
        return self._vac._attributes.get("device_type")
    @property
    def available(self):
        return self._vac.available
    async def async_update(self):
        await self._vac.async_update()

class IAquaLinkLastOnlineSensor(SensorEntity):
    def __init__(self, vac):
        self._vac = vac
        self._attr_name = f"{vac.name} Last Online"
    @property
    def state(self):
        return self._vac._attributes.get("last_online")
    @property
    def available(self):
        return self._vac.available
    async def async_update(self):
        await self._vac.async_update()

class IAquaLinkTemperatureSensor(SensorEntity):
    def __init__(self, vac):
        self._vac = vac
        self._attr_name = f"{vac.name} Temperature"
        self._attr_unit_of_measurement = "°F"
    @property
    def state(self):
        return self._vac.temperature
    @property
    def available(self):
        return self._vac.available
    async def async_update(self):
        await self._vac.async_update()

class IAquaLinkTotalHoursSensor(SensorEntity):
    def __init__(self, vac):
        self._vac = vac
        self._attr_name = f"{vac.name} Total Hours"
    @property
    def state(self):
        return self._vac._attributes.get("total_hours")
    @property
    def available(self):
        return self._vac.available
    async def async_update(self):
        await self._vac.async_update()

class IAquaLinkCycleStartSensor(SensorEntity):
    def __init__(self, vac):
        self._vac = vac
        self._attr_name = f"{vac.name} Cycle Start Time"
    @property
    def state(self):
        return self._vac._attributes.get("cycle_start_time")
    @property
    def available(self):
        return self._vac.available
    async def async_update(self):
        await self._vac.async_update()

class IAquaLinkCycleSensor(SensorEntity):
    def __init__(self, vac):
        self._vac = vac
        self._attr_name = f"{vac.name} Cycle Index"
    @property
    def state(self):
        return self._vac._attributes.get("cycle")
    @property
    def available(self):
        return self._vac.available
    async def async_update(self):
        await self._vac.async_update()

class IAquaLinkCycleDurationSensor(SensorEntity):
    def __init__(self, vac):
        self._vac = vac
        self._attr_name = f"{vac.name} Cycle Duration"
        self._attr_unit_of_measurement = "minutes"
    @property
    def state(self):
        return self._vac._attributes.get("cycle_duration")
    @property
    def available(self):
        return self._vac.available
    async def async_update(self):
        await self._vac.async_update()

class IAquaLinkCycleEndSensor(SensorEntity):
    def __init__(self, vac):
        self._vac = vac
        self._attr_name = f"{vac.name} Cycle End Time"
    @property
    def state(self):
        return self._vac._attributes.get("cycle_end_time")
    @property
    def available(self):
        return self._vac.available
    async def async_update(self):
        await self._vac.async_update()

class IAquaLinkTimeRemainingSensor(SensorEntity):
    def __init__(self, vac):
        self._vac = vac
        self._attr_name = f"{vac.name} Time Remaining"
    @property
    def state(self):
        return self._vac._attributes.get("time_remaining")
    @property
    def available(self):
        return self._vac.available
    async def async_update(self):
        await self._vac.async_update()

class IAquaLinkModelSensor(SensorEntity):
    def __init__(self, vac):
        self._vac = vac
        self._attr_name = f"{vac.name} Model"
    @property
    def state(self):
        return self._vac._attributes.get("model")
    @property
    def available(self):
        return self._vac.available
    async def async_update(self):
        await self._vac.async_update()

# ────── BinarySensor for Canister Full ──────

class IAquaLinkCanisterFullSensor(BinarySensorEntity):
    def __init__(self, vac):
        self._vac = vac
        self._attr_name = f"{vac.name} Canister Full"
    @property
    def is_on(self):
        # True if 'canister' count > 0
        return int(self._vac._attributes.get("canister", 0)) > 0
    @property
    def available(self):
        return self._vac.available
    async def async_update(self):
        await self._vac.async_update()
