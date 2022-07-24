import time
from logging import DEBUG

from bleson import (
    get_provider,
    Advertiser,
    Advertisement,
    LE_GENERAL_DISCOVERABLE,
    BREDR_NOT_SUPPORTED,
    set_level,
)

from ble_light.connector import BtBackend
from ble_light.encoder import Message


class BlesonBackend(BtBackend):
    def __init__(self):
        raise NotImplementedError

        set_level(DEBUG)
        adapter = get_provider().get_adapter()
        self.advertiser = Advertiser(adapter)

    def send_message(self, message: Message):
        advertisement = Advertisement()
        advertisement.flags = LE_GENERAL_DISCOVERABLE | BREDR_NOT_SUPPORTED
        advertisement.raw_data = b"0xFF" + message.hex_data
        print(advertisement.raw_data)
        self.advertiser.advertisement = advertisement

        for _ in range(2):
            self.advertiser.start()
            time.sleep(0.5)
            self.advertiser.stop()
