import asyncio
import json
import datetime
import aiohttp
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
    URL_LOGIN,
    URL_GET_DEVICES,
    URL_GET_DEVICE_STATUS,
    URL_GET_DEVICE_FEATURES,
    NAME,
    VERSION,
    DOMAIN,
    ISSUEURL,
    STARTUP,
    SCAN_INTERVAL
)

# Features your vacuum supports
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
        IAquaLinkErrorStateSensor(vacuum),
        IAquaLinkCleaningActiveSensor(vacuum),
    ]
    async_add_entities(entities)

class IAquaLinkRobotVacuum(StateVacuumEntity):
    """Represents an iaqualink_robots vacuum."""

    def __init__(self, config):
        """Initialize with the YAML config passed by HA."""
        super().__init__()
        self._name     = config.get("name")
        self._username = config.get("username")
        self._password = config.get("password")
        self._api_key  = config.get("api_key")

        # Basic state holders
        self._attributes         = {}
        self._activity           = VacuumActivity.IDLE
        self._status             = STATE_OFF
        self._supported_features = SUPPORT_FLAGS
        self._temperature        = None
        self._battery_level      = None

        # If you had more in your original __init__, paste it here!

    @property
    def name(self):
        return self._name

    @property
    def supported_features(self):
        return self._supported_features

    @property
    def state(self):
        # Map VacuumActivity to HA states if needed
        if self._activity == VacuumActivity.CLEANING:
            return STATE_ON
        return STATE_OFF

    @property
    def available(self):
        return True  # or more precise logic

    async def async_start(self):
        """Start vacuum logic here (your original code)."""
        pass

    async def async_stop(self, **kwargs):
        """Stop vacuum logic here (original code)."""
        pass

    async def async_update(self):
        """Fetch latest state/attributes."""
        # Paste your original async_update logic here, populating:
        #   self._attributes["username"], etc.
        #   self._temperature = ...
        #   self._activity = VacuumActivity.CLEANING/IDLE/etc.
        pass

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
        return True

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
        return True

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
        return True

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
        return True

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
        return True

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
        return True

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
        return True

    async def async_update(self):
        await self._vac.async_update()


class IAquaLinkTemperatureSensor(SensorEntity):
    def __init__(self, vac):
        self._vac = vac
        self._attr_name = f"{vac.name} Temperature"
        self._attr_unit_of_measurement = "°F"

    @property
    def state(self):
        return self._vac._temperature

    @property
    def available(self):
        return True

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
        return True

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
        return True

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
        return True

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
        return True

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
        return True

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
        return True

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
        return True

    async def async_update(self):
        await self._vac.async_update()


# ────────── BinarySensorEntity classes ──────────

class IAquaLinkCanisterFullSensor(BinarySensorEntity):
    def __init__(self, vac):
        self._vac = vac
        self._attr_name = f"{vac.name} Canister Full"

    @property
    def is_on(self):
        return int(self._vac._attributes.get("canister", 0)) > 0

    @property
    def available(self):
        return True

    async def async_update(self):
        await self._vac.async_update()


class IAquaLinkErrorStateSensor(BinarySensorEntity):
    def __init__(self, vac):
        self._vac = vac
        self._attr_name = f"{vac.name} Error State"

    @property
    def is_on(self):
        return int(self._vac._attributes.get("error_state", 0)) != 0

    @property
    def available(self):
        return True

    async def async_update(self):
        await self._vac.async_update()


class IAquaLinkCleaningActiveSensor(BinarySensorEntity):
    def __init__(self, vac):
        self._vac = vac
        self._attr_name = f"{vac.name} Cleaning Active"

    @property
    def is_on(self):
        return self._vac._activity == VacuumActivity.CLEANING

    @property
    def available(self):
        return True

    async def async_update(self):
        await self._vac.async_update()
