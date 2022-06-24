# Smart light app for GM Smart Light

Algorithm decompiled from Android app `GM Smart Light v0.0.3` (com.hm.simpleble)

For using you need to install and connect GM Smart Light http://le-iot.com/download/simble_gm_downshow.html

Then go to Settings and copy `Current ID (mode)` to `MAC` in app.py

![](.github/screen.png)

## Example:

```python
from ble_light.connector import App
from ble_light.encoder import Commands

MAC = "D6FFFFFC"

app = App(MAC)
app.send(Commands.turn_on())  # Turn on light
app.send(Commands.turn_off())  # turn off light
app.send(Commands.night())  # night mode
app.send(Commands.all_light())  # all light mode
app.send(Commands.bright(1000))  # brightness 0-1000
app.send(Commands.temp(3000))  # temperature 3000-6400
```