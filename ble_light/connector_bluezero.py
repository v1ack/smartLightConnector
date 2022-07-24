import time
from threading import Thread

from bluezero import advertisement
from bluezero.broadcaster import Beacon

from ble_light.connector import BtBackend
from ble_light.encoder import Message


class LeBeacon(Beacon):
    def start_beacon(self):
        if not self.dongle.powered:
            self.dongle.powered = True
        ad_manager = advertisement.AdvertisingManager(self.dongle.address)
        ad_manager.register_advertisement(self.broadcaster, {})

        thread = Thread(target=self.broadcaster.start)
        thread.start()
        time.sleep(0.5)

        self.broadcaster.stop()
        ad_manager.unregister_advertisement(self.broadcaster)


class BluezeroBackend(BtBackend):
    def __init__(self):
        self.beacon = LeBeacon()

    def send_message(self, message: Message):
        self.beacon.add_manufacturer_data(
            message.manufacturer_id, message.manufacturer_data
        )

        for _ in range(2):
            self.beacon.start_beacon()
