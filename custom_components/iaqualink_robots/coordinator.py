import asyncio
import json
import aiohttp
from datetime import timedelta
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from .const import URL_LOGIN, URL_GET_DEVICES, URL_GET_DEVICE_STATUS, URL_GET_DEVICE_FEATURES, SCAN_INTERVAL

class IAquaLinkCoordinator(DataUpdateCoordinator):
    """Manage fetching data from iAqualink."""

    def __init__(self, hass, entry):
        self.entry = entry
        self.username = entry.data["username"]
        self.password = entry.data["password"]
        self.api_key  = entry.data["api_key"]

        super().__init__(
            hass,
            _LOGGER,
            name=entry.title,
            update_interval=timedelta(seconds=SCAN_INTERVAL),
        )

    async def _async_update_data(self):
        """Fetch data from API."""
        try:
            # 1) Login
            payload = {"apikey": self.api_key, "email": self.username, "password": self.password}
            session = aiohttp.ClientSession()
            resp = await session.post(URL_LOGIN, json=payload)
            auth = await resp.json()
            token = auth["authentication_token"]
            user_id = auth["id"]
            session.headers.update({"Authorization": token})

            # 2) Get device list
            resp = await session.get(URL_GET_DEVICES, params={"authentication_token": token, "user_id": user_id, "api_key": self.api_key})
            devices = await resp.json()
            # pick first VR device:
            device = next(d for d in devices if d["device_type"] == "vr")
            serial = device["serial_number"]

            # 3) Get status via websocket or GET_DEVICE_STATUS logic...
            # (pseudo-code)
            status = {"status": "connected", "temperature": 25, "canister": 0, ...}

            # 4) Get model/features
            resp = await session.get(URL_GET_DEVICE_FEATURES + serial + "/features")
            features = await resp.json()

            await session.close()
            return {"device": device, "status": status, "features": features}
        except Exception as err:
            raise UpdateFailed(err)

