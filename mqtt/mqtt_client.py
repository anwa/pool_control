import paho.mqtt.client as mqtt
import json
from utils.logger import logger
from utils.config import config
from mqtt.topics import cmnd_topics


class MQTTClient:
    """
    Zentraler MQTT-Client für die gesamte Anwendung.
    Ermöglicht das Abonnieren mehrerer Topics mit Namen und das Senden von Kommandos.
    """

    def __init__(
        self,
        broker="10.10.1.30",
        port=1883,
        username=None,
        password=None,
        client_id="poolcontrol",
    ):
        broker = config.get("MQTT", "ip")
        port = config.get("MQTT", "port", type_cast=int)
        username = config.get("MQTT", "user")
        password = config.get("MQTT", "password")
        # MQTT-Client-Objekt erzeugen
        self.client = mqtt.Client()
        # Authentifizierung setzen, falls angegeben
        if username and password:
            self.client.username_pw_set(username, password)
        # Callback-Funktionen setzen
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        # Mapping: topic -> name (z.B. "GTN/Pool/Pumpe/tele/SENSOR" -> "pumpe_power")
        self.topic_to_name = {}
        # Mapping: name -> callback-Funktion
        self.name_to_callback = {}
        # Verbindung herstellen und Loop starten
        self.client.connect(broker, port, 60)
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        """
        Wird aufgerufen, wenn die Verbindung zum Broker hergestellt wurde.
        """
        if rc == 0:
            logger.info("MQTT: Verbindung erfolgreich!")
            for topic in cmnd_topics.values():
                # Leeres Payload fragt den Status ab (Tasmota-Logik)
                self.mqtt_client.publish(topic, payload="", qos=1, retain=False)
        else:
            logger.info(f"MQTT: Verbindungsfehler, Code {rc}")

    def on_message(self, client, userdata, msg):
        """
        Wird aufgerufen, wenn eine Nachricht auf einem abonnierten Topic empfangen wird.
        """
        topic = msg.topic
        payload = msg.payload.decode()
        name = self.topic_to_name.get(topic)
        logger.info(f"topic: {topic}; payload: {payload}; name: {name}")
        if name and name in self.name_to_callback:
            # Versuche, das JSON zu parsen
            try:
                data = json.loads(payload)
                # Beispiel: Extrahiere "Power" aus "ENERGY" für das Pumpen-Topic
                if "ENERGY" in data and "Power" in data["ENERGY"]:
                    value = data["ENERGY"]["Power"]
                else:
                    value = data  # Fallback: ganzes JSON
                # Callback aufrufen: (name, value)
                self.name_to_callback[name](name, value)
            except Exception as e:
                logger.info(f"MQTT: Fehler beim Parsen von {topic}: {e}")

    def subscribe_dict(self, name_topic_dict, callback):
        """
        Abonniert alle Topics aus dem Dictionary und ruft für jede empfangene Nachricht
        die Callback-Funktion mit (name, value) auf.
        :param name_topic_dict: dict, z.B. {"pumpe_power": "GTN/Pool/Pumpe/tele/SENSOR"}
        :param callback: Funktion mit Signatur callback(name, value)
        """
        for name, topic in name_topic_dict.items():
            self.topic_to_name[topic] = name
            self.name_to_callback[name] = callback
            self.client.subscribe(topic)

    def publish(self, topic, payload):
        """
        Sendet eine Nachricht an das angegebene Topic.
        :param topic: Topic-String
        :param payload: String oder serialisiertes JSON
        """
        self.client.publish(topic, payload)


# Singleton-Instanz für die gesamte Anwendung
mqtt_client = MQTTClient()


#    def __init__(self, broker, port, user, password, client_id="poolcontrol"):
#        self.client = mqtt.Client(client_id)

#    def send_autodiscovery(
#        self, sensor_name, unique_id, unit, device_class, state_topic
#    ):
#        topic = f"homeassistant/sensor/{unique_id}/config"
#        payload = {
#            "name": sensor_name,
#            "state_topic": state_topic,
#            "unit_of_measurement": unit,
#            "device_class": device_class,
#            "unique_id": unique_id,
#            "availability_topic": "poolcontrol/status",
#        }
#        self.publish(topic, payload, retain=True)
