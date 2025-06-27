from utils.logger import logger
from utils.config import config
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, NumericProperty  # , BooleanProperty

from mqtt.mqtt_client import mqtt_client
from mqtt.topics import mess_topics

Builder.load_file("gui/messung.kv")


class MessungPage(BoxLayout):
    # Properties für Messwerte
    ph_value = StringProperty("7.2")
    pool_temp = StringProperty("24.5 °C")
    tds_value = StringProperty("800 ppm")
    pool_power = StringProperty("2975 W")
    pool_energy_today = StringProperty("11.30 kWh")
    pool_energy_yesterday = StringProperty("21.65 kWh")
    wp_current_temp = StringProperty("0")
    wp_target_temp = StringProperty("0")
    pool_temp   = NumericProperty(0.0)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Konfigurationswerte setzen
        self.pool_liter = config.get("Pool", "liter", fallback="unbekannt")
        self.ph_sollwert = config.get("PH", "sollwert", fallback="unbekannt")
        self.ph_liquid = config.get("PH", "liquid", fallback="unbekannt")
        self.ph_konzentration = config.get("PH", "konzentration", fallback="unbekannt")
        # MQTT-Subscribe
        mqtt_client.subscribe_dict(mess_topics, self.on_mqtt_value)

    def on_mqtt_value(self, name, value):
        Clock.schedule_once(lambda dt: self._update_value(name, value))

    def _update_value(self, name, value):
        if name == "wp_current_temp":
            self.wp_current_temp = f"{value:.0f}"
        if name == "wp_target_temp":
            self.wp_target_temp = f"{value:.0f}"
        if name == "pool_temp":
            self.pool_temp = value
            
