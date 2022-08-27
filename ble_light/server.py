from dataclasses import dataclass
from os import getenv
from typing import Optional

from fastapi import FastAPI, HTTPException

from ble_light.connector import App
from ble_light.connector_bless import BlessBackend
from ble_light.encoder import Commands


@dataclass
class ProxyApp:
    app: App
    is_on: bool = False
    brightness = 1000
    temp = 6000

    def send(self, command: str, value: Optional[int] = None):
        command_func = getattr(Commands, command)
        self.app.send(command_func(value) if value is not None else command_func())
        if command == "bright":
            self.brightness = value
        elif command == "temp":
            self.temp = value
        elif command == "turn_off":
            self.is_on = False
        elif command == "turn_on":
            self.is_on = True

    def get_state(self) -> dict:
        return {
            "is_on": self.is_on,
            "brightness": self.brightness,
            "temp": self.temp,
        }


app = FastAPI()

mac = getenv("MAC")
print(f'"{mac}"')
le_app = ProxyApp(app=App(mac, BlessBackend()))


@app.post("/lamp")
async def update_item(command: str, value: Optional[int] = None):
    if command == "turn_on" and le_app.is_on:
        return {"status": "already on"}
    elif command == "turn_off" and not le_app.is_on:
        return {"status": "already off"}
    try:
        le_app.send(command, value)
    except AttributeError:
        raise HTTPException(status_code=404, detail="Command not found")

    return {"ok": True}


@app.get("/lamp")
async def read_item():
    return le_app.get_state()
