from ble_light.connector import App
from ble_light.encoder import Commands
from ble_light.connector_bleson import BlesonBackend

if __name__ == "__main__":
    MAC = "D6FFFFFC"

    app = App(MAC, BlesonBackend())
    # app.send(Commands.turn_on())
    # app.send(Commands.bright(1000))
    app.send(Commands.turn_off())
