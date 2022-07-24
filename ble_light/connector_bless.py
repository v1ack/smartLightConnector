import asyncio
from asyncio import sleep

from bless import BlessServer
from bless.backends.bluezdbus.dbus.advertisement import BlueZLEAdvertisement, Type
from bless.backends.bluezdbus.server import BlessServerBlueZDBus

from ble_light.connector import BtBackend
from ble_light.encoder import Message


class BlessServer(BlessServerBlueZDBus):
    async def send_message(self, message: Message, timeout=0.5):
        # start advertising
        await self.app.set_name(self.adapter, self.name)
        advertisement = BlueZLEAdvertisement(Type.BROADCAST, 0, self.app)
        advertisement.ManufacturerData = {
            message.manufacturer_id: message.manufacturer_data
        }
        self.app.advertisements = [advertisement]

        self.bus.export(advertisement.path, advertisement)

        iface = self.adapter.get_interface("org.bluez.LEAdvertisingManager1")
        await iface.call_register_advertisement(advertisement.path, {})  # type: ignore

        # await
        await sleep(timeout)

        # stop advertising
        await self.app.set_name(self.adapter, "")
        advertisement: BlueZLEAdvertisement = self.app.advertisements.pop()
        iface = self.adapter.get_interface("org.bluez.LEAdvertisingManager1")
        await iface.call_unregister_advertisement(advertisement.path)  # type: ignore


class BlessBackend(BtBackend):
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.server = BlessServer(name="my_service_name", loop=self.loop)

    async def _send_message(self, message: Message):
        for _ in range(2):
            await self.server.send_message(message, timeout=0.5)

    def send_message(self, message: Message):
        self.loop.run_until_complete(self.server.send_message(message))
