import time
from threading import Thread

from bluezero import advertisement, adapter
from bluezero.broadcaster import Beacon

from ble_light.connector import BtBackend
from ble_light.encoder import Message


class LeBeacon(Beacon):
    def __init__(self, adapter_addr=None):
        """Default initialiser.

        Creates the BLE beacon object
        If an adapter object exists then give it as an optional argument
        If an adapter object is not given then the first adapter found is used
        :param adapter_addr: Optional Python adapter object.
        """
        self.dongle = None
        if adapter_addr is None:
            self.dongle = adapter.Adapter(adapter.list_adapters()[0])
        else:
            self.dongle = adapter.Adapter(adapter_addr)

        self.broadcaster = advertisement.Advertisement(2, "broadcast")

    def start_beacon(self):
        if not self.dongle.powered:
            self.dongle.powered = True
        ad_manager = advertisement.AdvertisingManager(self.dongle.address)
        ad_manager.register_advertisement(self.broadcaster, {})

        thread = Thread(target=self.broadcaster.start)
        thread.start()
        time.sleep(0.1)

        self.broadcaster.stop()
        ad_manager.unregister_advertisement(self.broadcaster)

    def close(self):
        self.dongle.quit()


class BluezeroBackend(BtBackend):
    def __init__(self):
        self.beacon = LeBeacon()

    def send_message(self, message: Message):
        self.beacon.add_manufacturer_data(
            message.manufacturer_id, message.manufacturer_data
        )

        for _ in range(2):
            self.beacon.start_beacon()

    def close(self):
        self.beacon.close()
