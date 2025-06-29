# import kivy module
import kivy

kivy.require("2.3.1")

from utils.logger import logger
from sensors.one_wire import OneWireReader
from utils.config import config
from kivy.app import App
from kivy.config import Config
from kivy.lang import Builder

# from kivy.clock import Clock
from gui.missing_sensor_popup import MissingSensorPopup
from gui.new_sensor_popup import NewSensorPopup
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
        self.title = "Pool Control"
        self.icon = "gui/icons/pool.png"
        Builder.load_file("gui/main.kv")
        # self.root = MainScreen()
        # Clock.schedule_interval(self.root.update_time, 1)
        # return self.root
        return MainScreen()

    def on_start(self):
        logger.info("Application started.")
        self.reader = OneWireReader()
        self.missing_sensors = self.reader.get_missing_sensors()
        self._show_next_missing_sensor()
        self._show_next_new_sensor()

    def _show_next_new_sensor(self):
        if not self.new_sensors:
            return

        sensor_id, temp = self.new_sensors.pop(0)

        # Mögliche Namen, die noch nicht vergeben sind
        all_names = ["Pool", "PH_IN", "PH_OUT", "WP_OUT"]
        used_names = set(self.reader.id_to_name.values())
        available_names = [n for n in all_names if n not in used_names]

        popup = NewSensorPopup(
            sensor_id=sensor_id,
            temperature=temp,
            available_names=available_names,
            assign_callback=self._handle_sensor_assignment
        )
        popup.open()

    def _handle_sensor_assignment(self, sensor_id, name):
        if name:
            self.reader.assign_name(sensor_id, name)
        else:
            self.reader.ignore_sensor(sensor_id)
        self._show_next_new_sensor()
        
    def _show_next_missing_sensor(self):
        if not self.missing_sensors:
            return  # alle Sensoren verarbeitet

        sensor_id = self.missing_sensors.pop(0)
        sensor_name = config.get_onewire_mapping().get(sensor_id, sensor_id)

        popup = MissingSensorPopup(
            sensor_name=sensor_name,
            sensor_id=sensor_id,
            callback=self._handle_sensor_decision
        )
        popup.open()

    def _handle_sensor_decision(self, sensor_id, action):
        if action == "delete":
            config.delete_sensor(sensor_id)
        elif action == "ignore":
            self.reader.ignore_sensor(sensor_id)
        # "keep" → nichts tun

        self._show_next_missing_sensor()  # nächsten Sensor anzeigen

    def on_stop(self):
        logger.info("Application stopped.")


if __name__ == "__main__":
    logger.info("Starte Pool Control mit folgender Konfiguration:")
    logger.info(f"MQTT-Server: {config.get('MQTT', 'ip')}:{config.get('MQTT', 'port')}")
    logger.info(f"Pool Liter: {config.get('Pool', 'liter')}")
    logger.info(f"PH-Sollwert: {config.get('PH', 'sollwert')}")
    logger.info(f"1-Wire: {config.get_onewire_mapping()}")
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
