from utils.logger import logger
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, BooleanProperty
from kivy.clock import Clock
from datetime import datetime
from utils.network import get_ip, get_wifi_strength
from mqtt.mqtt_client import mqtt_client
from mqtt.topics import cmnd_topics, relay_topics

# import paho.mqtt.client as mqtt
# import json
from gui.info import InfoPage
from gui.messung import MessungPage
from gui.settings import SettingsPage


class MainScreen(BoxLayout):
    # Properties für Kopfbereich
    date_time = StringProperty()
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
    # Properties für Fußbereich
    ip_address = StringProperty("192.168.1.100")
    wifi_strength = StringProperty("-60 dBm")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.update_time(0)
        self.date_time = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        self.ip_address = get_ip()
        self.wifi_strength = str(get_wifi_strength())

        # Zeit jede Sekunde aktualisieren
        Clock.schedule_interval(self.update_time, 1)
        # IP alle 10 Minuten (600 Sekunden) aktualisieren
        Clock.schedule_interval(self.update_ip, 600)
        # WLAN alle 30 Sekunden aktualisieren
        Clock.schedule_interval(self.update_wifi, 10)
        # Lade InfoPage beim Start
        Clock.schedule_once(self.show_info, 0)
        # Nach 10 Sekunden auf Messung wechseln
        Clock.schedule_once(self.show_messung, 10)
        # MQTT-Subscribe
        mqtt_client.subscribe_dict(relay_topics, self.on_mqtt_value)

    def on_mqtt_value(self, name, value):
        Clock.schedule_once(lambda dt: self._update_value(name, value))

    def _update_value(self, name, value):
        setattr(self, name, str(value))

    """
    def on_mqtt_message(self, client, userdata, msg):
        if msg.topic == "GTN/Pool/Pumpe/tele/SENSOR":
            try:
                data = json.loads(msg.payload.decode())
                # ENERGY kann fehlen, daher absichern:
                energy = data.get("ENERGY", {})
                power = energy.get("Power")
                if power is not None:
                    logger.info(f"Aktuelle Pumpenleistung: {power} W")
                    # In Kivy-Property schreiben
                    self.pumpe_power = f"{power} W"
                else:
                    logger.info("Power-Wert nicht gefunden!")
                    self.pumpe_power = "?"
            except Exception as e:
                logger.info(f"Fehler beim Parsen: {e}")
                self.pumpe_power = "?"
    """

    def update_time(self, dt):
        self.date_time = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

    def update_ip(self, dt):
        self.ip_address = get_ip()

    def update_wifi(self, dt):
        self.wifi_strength = str(get_wifi_strength())

    def show_page(self, page_name):
        # Hier kannst du die Seitenumschaltung implementieren
        logger.info(f"Seite wechseln zu: {page_name}")
        center_area = self.ids.center_area
        center_area.clear_widgets()
        if page_name == "main":
            center_area.add_widget(MessungPage())
        elif page_name == "settings":
            center_area.add_widget(SettingsPage())
        elif page_name == "info":
            center_area.add_widget(InfoPage())

    def show_info(self, dt):
        self.show_page("info")

    def show_messung(self, dt):
        self.show_page("main")

    def toggle_relay(self, relay_name, state):
        cmd = "ON" if state else "OFF"
        topic = cmnd_topics.get(relay_name)
        if topic:
            mqtt_client.publish(topic, cmd)
            logger.info(f"Relais {relay_name} auf {state} gesetzt")
        else:
            logger.info(f"Unbekanntes Relais: {relay_name}")
