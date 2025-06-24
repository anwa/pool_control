from utils.logger import logger
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, BooleanProperty
from kivy.clock import Clock
from datetime import datetime
from utils.network import get_ip, get_wifi_strength
import paho.mqtt.client as mqtt
import json


class MainScreen(BoxLayout):
    # Properties für Kopfbereich
    date_time = StringProperty()
    # Properties für Messwerte
    ph_value = StringProperty("7.2")
    pool_temp = StringProperty("24.5 °C")
    tds_value = StringProperty("800 ppm")
    pool_power = StringProperty("2975 W")
    pool_energy_today = StringProperty("11.30 kWh")
    pool_energy_yesterday = StringProperty("21.65 kWh")
    wp_current_temp = StringProperty("")
    wp_target_temp = StringProperty("")
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
        Clock.schedule_interval(self.update_wifi, 30)

        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = self.on_mqtt_connect
        self.mqtt_client.on_message = self.on_mqtt_message
        self.mqtt_client.username_pw_set("homeassistant", "t4aFDfCNRzqcbb5bUB9y9jcC")
        self.mqtt_client.connect("10.10.1.30", 1883, 60)
        self.mqtt_client.loop_start()
        # Subscribe auf Status-Topic
        self.mqtt_client.subscribe("GTN/Pool/Pumpe/stat/POWER")
        self.mqtt_client.subscribe("GTN/Pool/Pumpe/tele/SENSOR")
        self.mqtt_client.subscribe("GTN/Pool/UV/stat/POWER")
        self.mqtt_client.subscribe("GTN/Pool/UV/tele/SENSOR")
        self.mqtt_client.subscribe("GTN/Pool/Salz/stat/POWER")
        self.mqtt_client.subscribe("GTN/Pool/Salz/tele/SENSOR")
        self.mqtt_client.subscribe("GTN/Pool/WP/stat/POWER")
        self.mqtt_client.subscribe("GTN/Pool/WP/tele/SENSOR")
        self.mqtt_client.subscribe("GTN/Pool/Licht/stat/POWER")
        self.mqtt_client.subscribe("GTN/Pool/Haus-Licht/stat/POWER")

    def on_mqtt_connect(self, client, userdata, flags, rc):
        logger.info(f"Connected to MQTT Broker with code: {rc}")
        self.mqtt_client.publish("GTN/Pool/Pumpe/cmnd/Power1", payload="", qos=1, retain=False)
        self.mqtt_client.publish("GTN/Pool/UV/cmnd/Power1", payload="", qos=1, retain=False)
        self.mqtt_client.publish("GTN/Pool/Salz/cmnd/Power1", payload="", qos=1, retain=False)
        self.mqtt_client.publish("GTN/Pool/WP/cmnd/Power1", payload="", qos=1, retain=False)
        self.mqtt_client.publish("GTN/Pool/Licht/cmnd/Power1", payload="", qos=1, retain=False)
        self.mqtt_client.publish("GTN/Pool/Haus-Licht/cmnd/Power1", payload="", qos=1, retain=False)

    def on_mqtt_message(self, client, userdata, msg):
        topic = msg.topic
        payload = msg.payload.decode()
        logger.info(f"Topic: {topic} | payload: {payload}")
        if topic == "GTN/Pool/Controller/stat/target_temp":
            self.wp_target_temp = payload
        if topic == "GTN/Pool/Controller/tele/current_temp":
            self.wp_current_temp = payload

        if topic == "GTN/Pool/Pumpe/stat/POWER":
            # Tasmota: "ON" oder "OFF"
            self.pumpe_state = payload == "ON"
        if topic == "GTN/Pool/UV/stat/POWER":
            # Tasmota: "ON" oder "OFF"
            self.uv_state = payload == "ON"
        if topic == "GTN/Pool/Salz/stat/POWER":
            # Tasmota: "ON" oder "OFF"
            self.elektrolyse_state = payload == "ON"
        if topic == "GTN/Pool/WP/stat/POWER":
            # Tasmota: "ON" oder "OFF"
            self.wp_state = payload == "ON"
        if topic == "GTN/Pool/Licht/stat/POWER":
            # Tasmota: "ON" oder "OFF"
            self.licht_state = payload == "ON"
        if topic == "GTN/Pool/Haus-Licht/stat/POWER":
            # Tasmota: "ON" oder "OFF"
            self.hlicht_state = payload == "ON"
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
        if msg.topic == "GTN/Pool/Salz/tele/SENSOR":
            try:
                data = json.loads(msg.payload.decode())
                # ENERGY kann fehlen, daher absichern:
                energy = data.get("ENERGY", {})
                power = energy.get("Power")
                if power is not None:
                    logger.info(f"Aktuelle Salz-Elektrolyse Leistung: {power} W")
                    # In Kivy-Property schreiben
                    self.elektrolyse_power = f"{power} W"
                else:
                    logger.info("Power-Wert nicht gefunden!")
                    self.elektrolyse_power = "?"
            except Exception as e:
                logger.info(f"Fehler beim Parsen: {e}")
                self.elektrolyse_power = "?"
        if msg.topic == "GTN/Pool/UV/tele/SENSOR":
            try:
                data = json.loads(msg.payload.decode())
                # ENERGY kann fehlen, daher absichern:
                energy = data.get("ENERGY", {})
                power = energy.get("Power")
                if power is not None:
                    logger.info(f"Aktuelle UV Leistung: {power} W")
                    # In Kivy-Property schreiben
                    self.uv_power = f"{power} W"
                else:
                    logger.info("Power-Wert nicht gefunden!")
                    self.uv_power = "?"
            except Exception as e:
                logger.info(f"Fehler beim Parsen: {e}")
                self.uv_power = "?"
        if msg.topic == "GTN/Pool/WP/tele/SENSOR":
            try:
                data = json.loads(msg.payload.decode())
                # ENERGY kann fehlen, daher absichern:
                energy = data.get("ENERGY", {})
                power = energy.get("Power")
                if power is not None:
                    logger.info(f"Aktuelle Wärmepumpen Leistung: {power} W")
                    # In Kivy-Property schreiben
                    self.wp_power = f"{power} W"
                else:
                    logger.info("Power-Wert nicht gefunden!")
                    self.wp_power = "?"
            except Exception as e:
                logger.info(f"Fehler beim Parsen: {e}")
                self.wp_power = "?"


    def update_time(self, dt):
        self.date_time = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

    def update_ip(self, dt):
        self.ip_address = get_ip()

    def update_wifi(self, dt):
        self.wifi_strength = str(get_wifi_strength())

    def show_page(self, page_name):
        # Hier kannst du die Seitenumschaltung implementieren
        logger.info(f"Seite wechseln zu: {page_name}")

    def toggle_relay(self, relay_name, state):
        # Hier kannst du die Relaissteuerung implementieren
        logger.info(f"Relais {relay_name} auf {state} gesetzt")

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
