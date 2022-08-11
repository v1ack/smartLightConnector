"""Platform for light integration."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.light import (
    ATTR_BRIGHTNESS,
    ATTR_COLOR_TEMP,
    LightEntity,
    ColorMode,
)
from homeassistant.helpers.entity import DeviceInfo
import requests

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    # Получаем ссылку на родительский класс нашей интеграции из конфигурации модуля.
    light = hass.data[DOMAIN][config_entry.entry_id]
    async_add_entities([light])


def normalize_value(value: int, max: int, new_max: int) -> int:
    """Normalize value to new range."""
    return int(value * new_max / max)


class LeLight(LightEntity):
    min_mireds = 3000
    max_mireds = 6400

    _attr_unique_id = "lelight_light"

    supported_color_modes = {
        ColorMode.ONOFF,
        ColorMode.BRIGHTNESS,
        ColorMode.COLOR_TEMP,
    }

    def __init__(self, host: str) -> None:
        self._host = host
        self._name = "LeLight"
        self._state = False
        self._brightness = 255
        self._temp = 4700

    @property
    def name(self) -> str:
        return self._name

    @property
    def brightness(self):
        return normalize_value(self._brightness, 1000, 255)

    @property
    def color_temp(self) -> int | None:
        return self._temp

    @property
    def color_mode(self) -> ColorMode | None:
        return ColorMode.COLOR_TEMP

    def turn_on(self, **kwargs: Any) -> None:
        requests.post(f"{self._host}/lamp?command=turn_on")
        if ATTR_BRIGHTNESS in kwargs:
            self._brightness = normalize_value(
                kwargs.get(ATTR_BRIGHTNESS, 255), 255, 1000
            )
            requests.post(f"{self._host}/lamp?command=bright&value={self._brightness}")
        if ATTR_COLOR_TEMP in kwargs:
            self._temp = kwargs.get(ATTR_COLOR_TEMP, 4700)
            requests.post(f"{self._host}/lamp?command=temp&value={self._temp}")

    def turn_off(self, **kwargs: Any) -> None:
        requests.post(f"{self._host}/lamp?command=turn_off")

    def update(self) -> None:
        """Fetch new state data for this light.

        This is the only method that should fetch new data for Home Assistant.
        """
        data = requests.get(f"{self._host}/lamp").json()
        self._state = data["is_on"]
        self._brightness = normalize_value(data["brightness"], 255, 1000)
        self._temp = data["temp"]

    def is_on(self) -> bool:
        return self._state

    @property
    def device_info(self) -> DeviceInfo | None:
        return {
            "identifiers": {(DOMAIN, self._host)},
            "name": "lelight lamp",
            "sw_version": "none",
            "model": "lelight lamp",
            "manufacturer": "lelight",
        }
