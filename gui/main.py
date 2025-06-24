from utils.logger import logger
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, BooleanProperty
from kivy.clock import Clock
from datetime import datetime
from utils.network import get_ip, get_wifi_strength
import paho.mqtt.client as mqtt


class MainScreen(BoxLayout):
    # Properties für Kopfbereich
    date_time = StringProperty()
    # Properties für Messwerte
    ph_value = StringProperty("7.2")
    pool_temp = StringProperty("24.5 °C")
    tds_value = StringProperty("800 ppm")
    # Properties für Relais-Schalter
    pumpe_state = BooleanProperty(False)
    uv_state = BooleanProperty(False)
    elektrolyse_state = BooleanProperty(False)
    wp_state = BooleanProperty(False)
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
        Clock.schedule_interval(self.update_wifi, 30)

        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = self.on_mqtt_connect
        self.mqtt_client.on_message = self.on_mqtt_message
        # self.mqtt_client.connect("10.10.1.30", 1883, 60)
        # self.mqtt_client.loop_start()
        # Subscribe auf Status-Topic
        # self.mqtt_client.subscribe("GTN/Pool/Pumpe/stat/POWER")
        # self.mqtt_client.subscribe("GTN/Pool/UV/stat/POWER")
        # self.mqtt_client.subscribe("GTN/Pool/Salz/stat/POWER")
        # self.mqtt_client.subscribe("GTN/Pool/Licht/stat/POWER")
        # self.mqtt_client.subscribe("GTN/Pool/Haus-Licht/stat/POWER")
        # self.mqtt_client.subscribe("GTN/Pool/WP/stat/POWER")

    def on_mqtt_connect(self, client, userdata, flags, rc):
        print("MQTT verbunden")

    def on_mqtt_message(self, client, userdata, msg):
        topic = msg.topic
        payload = msg.payload.decode()
        if topic == "GTN/Pool/Pumpe/stat/POWER":
            # Tasmota: "ON" oder "OFF"
            self.pumpe_state = payload == "ON"
        if topic == "GTN/Pool/UV/stat/POWER":
            # Tasmota: "ON" oder "OFF"
            self.uv_state = payload == "ON"
        if topic == "GTN/Pool/Salz/stat/POWER":
            # Tasmota: "ON" oder "OFF"
            self.elektrolyse_state = payload == "ON"
        if topic == "GTN/Pool/Licht/stat/POWER":
            # Tasmota: "ON" oder "OFF"
            self.licht_state = payload == "ON"
        if topic == "GTN/Pool/Haus-Licht/stat/POWER":
            # Tasmota: "ON" oder "OFF"
            self.hlicht_state = payload == "ON"
        if topic == "GTN/Pool/WP/stat/POWER":
            # Tasmota: "ON" oder "OFF"
            self.wp_state = payload == "ON"

    def update_time(self, dt):
        self.date_time = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

    def update_ip(self, dt):
        self.ip_address = get_ip()

    def update_wifi(self, dt):
        self.wifi_strength = str(get_wifi_strength())

    def show_page(self, page_name):
        # Hier kannst du die Seitenumschaltung implementieren
        print(f"Seite wechseln zu: {page_name}")

    def toggle_relay(self, relay_name, state):
        # Hier kannst du die Relaissteuerung implementieren
        print(f"Relais {relay_name} auf {state} gesetzt")
        # Beispiel: Property setzen
        if relay_name == "pumpe":
            # Sende MQTT-Kommando, aber setze pumpe_state NICHT direkt!
            cmd = "ON" if state else "OFF"
            self.mqtt_client.publish("GTN/Pool/Pumpe/cmnd/Power1", cmd)
            # Optional: Timeout/Fehlerbehandlung, falls keine Rückmeldung kommt
        elif relay_name == "uv":
            cmd = "ON" if state else "OFF"
            self.mqtt_client.publish("GTN/Pool/UV/cmnd/Power1", cmd)
        elif relay_name == "elektrolyse":
            cmd = "ON" if state else "OFF"
            self.mqtt_client.publish("GTN/Pool/Salz/cmnd/Power1", cmd)
        elif relay_name == "wp":
            cmd = "ON" if state else "OFF"
            self.mqtt_client.publish("GTN/Pool/WP/cmnd/Power1", cmd)
        elif relay_name == "licht":
            cmd = "ON" if state else "OFF"
            self.mqtt_client.publish("GTN/Pool/Licht/cmnd/Power1", cmd)
        elif relay_name == "hlicht":
            cmd = "ON" if state else "OFF"
            self.mqtt_client.publish("GTN/Pool/Haus-Licht/cmnd/Power1", cmd)
