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
    ph_value = NumericProperty(7.2)

    pool_temp   = NumericProperty(0.0)
    poolhaus_in_temp   = NumericProperty(0.0)
    waermepumpe_out_temp   = NumericProperty(0.0)
    poolhaus_out_temp   = NumericProperty(0.0)
    poolhaus_temp   = NumericProperty(0.0)
    wp_current_temp = NumericProperty(0.0)
    wp_target_temp = NumericProperty(0.0)

    tds_value = NumericProperty(800)
    power = NumericProperty(0.0)
    energy_today = NumericProperty(0.0)
    energy_yesterday = NumericProperty(0.0)
    p_in = NumericProperty(0.0)
    p_out = NumericProperty(0.0)
    p_diff = NumericProperty(0.0)

    out_temp = NumericProperty(0.0)
    out_hum = NumericProperty(0.0)
    out_press = NumericProperty(0.0)

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
        setattr(self, name, value)
        if name == "p_in" or name == "p_out":
            self.p_diff = self.p_out - self.p_in
