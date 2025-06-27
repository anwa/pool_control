# import kivy module
import kivy

kivy.require("2.3.1")

from utils.logger import logger
from utils.config import config
from kivy.app import App
from kivy.config import Config
from kivy.lang import Builder

# from kivy.clock import Clock
from gui.main import MainScreen

# sudo raspi-config
# Display Options -> Resolution -> DMT Mode 87 1024x600 60Hz
Config.set("graphics", "width", "1024")
Config.set("graphics", "height", "600")
Config.set("graphics", "resizable", "0")
Config.set("graphics", "borderless", "1")
# Uncomment on final setup
# Config.set("graphics", "show_cursor", "0")    # Mauszeiger ausblenden
# Config.set('graphics', 'fullscreen', 'auto')  # oder '1'


class PoolControlApp(App):
    def build(self):
        logger.info("Application started.")
        self.title = "Pool Control"
        self.icon = "gui/icons/pool.png"
        Builder.load_file("gui/main.kv")
        # self.root = MainScreen()
        # Clock.schedule_interval(self.root.update_time, 1)
        # return self.root
        return MainScreen()

    def on_stop(self):
        logger.info("Application stopped.")


if __name__ == "__main__":
    logger.info("Starte Pool Control mit folgender Konfiguration:")
    logger.info(f"MQTT-Server: {config.get('MQTT', 'ip')}:{config.get('MQTT', 'port')}")
    logger.info(f"Pool Liter: {config.get('Pool', 'liter')}")
    logger.info(f"PH-Sollwert: {config.get('PH', 'sollwert')}")
    PoolControlApp().run()

# from sensors.mcp23017_io import MCP23017IO, InputName, OutputName
#
# mcp = MCP23017IO()
#
## Eingänge lesen
# alle_eingaenge = mcp.read_inputs()
# uv_eingang = mcp.read_inputs(InputName.UV)
# salz_eingang = mcp.read_inputs("salz")
# pumpe_eingang = mcp.read_inputs(3)
#
## Ausgänge lesen
# alle_ausgaenge = mcp.read_outputs()
# pumpe_ausgang = mcp.read_outputs(OutputName.PUMPE)
# uv_ausgang = mcp.read_outputs("uv")
# wp_ausgang = mcp.read_outputs(3)
#
## Ausgänge setzen
# mcp.set_output(OutputName.PUMPE, True)
# mcp.set_output("uv", False)
# mcp.set_output(2, True)
