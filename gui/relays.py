from utils.logger import logger
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, BooleanProperty
from kivy.clock import Clock
from kivy.lang import Builder
from mqtt.mqtt_client import mqtt_client
from mqtt.topics import cmnd_topics, relay_topics

Builder.load_file("gui/relays.kv")


class RelaysView(BoxLayout):
    # Properties für Relais-Schalter
    pumpe_state = BooleanProperty(False)
    pumpe_power = StringProperty("450 W")
    uv_state = BooleanProperty(False)
    uv_power = StringProperty("75 W")
    elektrolyse_state = BooleanProperty(False)
    elektrolyse_power = StringProperty("100 W")
    wp_state = BooleanProperty(False)
    wp_power = StringProperty("2350 W")
    licht_state = BooleanProperty(False)
    hlicht_state = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # MQTT-Subscribe
        mqtt_client.subscribe_dict(relay_topics, self.on_mqtt_value)
        for topic in cmnd_topics.values():
            mqtt_client.publish(topic, payload="", qos=1, retain=False)

    def on_mqtt_value(self, name, value):
        Clock.schedule_once(lambda dt: self._update_value(name, value))

    def _update_value(self, name, value):
        if value == "ON":
            setattr(self, name, True)
        elif value == "OFF":
            setattr(self, name, False)
        else:
            setattr(self, name, str(value))

    def toggle_relay(self, relay_name, state):
        cmd = "ON" if state else "OFF"
        topic = cmnd_topics.get(relay_name)
        if topic:
            mqtt_client.publish(topic, cmd)
            logger.info(f"Relais {relay_name} auf {state} gesetzt")
        else:
            logger.info(f"Unbekanntes Relais: {relay_name}")
