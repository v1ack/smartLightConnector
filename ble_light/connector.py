from abc import abstractmethod

from ble_light.encoder import Command, Encryptor, Message


class BtBackend:
    @abstractmethod
    def send_message(self, message: Message):
        pass

    @abstractmethod
    def close(self):
        pass


class App:
    def __init__(self, mac: str, backend: BtBackend):
        _mac = list(
            map(
                lambda x: int.from_bytes(x, "big", signed=True),
                map(
                    lambda x: x.to_bytes(1, "little", signed=False),
                    bytearray.fromhex(mac),
                ),
            )
        )
        self.encryptor = Encryptor(_mac)
        self.backend = backend

    def _make_message(self, command: Command) -> Message:
        return self.encryptor.message(command)

    def send(self, command: Command):
        # Send commands twice
        self.backend.send_message(self._make_message(command))
        self.backend.send_message(self._make_message(command))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.backend.close()
