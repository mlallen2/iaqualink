"""Constants used by IaqualinkRobots."""
import json
from datetime import timedelta
from pathlib import Path
from typing import Final

from homeassistant.const import Platform
from homeassistant.components.vacuum import VacuumEntityFeature

PLATFORMS: Final = [
    Platform.VACUUM,
    Platform.SENSOR,
    Platform.BINARY_SENSOR,
]

# Which vacuum commands your robot supports
SUPPORT_FLAGS: Final = (
    VacuumEntityFeature.START
    | VacuumEntityFeature.STOP
    | VacuumEntityFeature.FAN_SPEED
    | VacuumEntityFeature.STATUS
    | VacuumEntityFeature.RETURN_HOME
)

URL_LOGIN               = "https://prod.zodiac-io.com/users/v1/login"
URL_GET_DEVICES         = "https://r-api.iaqualink.net/devices.json"
URL_GET_DEVICE_STATUS   = "https://prod.zodiac-io.com/devices/v1/"
URL_GET_DEVICE_FEATURES = "https://prod.zodiac-io.com/devices/v2/"

SCAN_INTERVAL = timedelta(seconds=30)

# Load manifest values
manifestfile = Path(__file__).parent / "manifest.json"
with open(manifestfile) as json_file:
    manifest_data = json.load(json_file)

DOMAIN   = manifest_data["domain"]
NAME     = manifest_data["name"]
VERSION  = manifest_data["version"]
ISSUEURL = manifest_data.get("issue_tracker", "")

STARTUP = f"""
-------------------------------------------------------------------
{NAME}
Version: {VERSION}
This is a custom component
If you have any issues, open one here:
{ISSUEURL}
-------------------------------------------------------------------
"""
