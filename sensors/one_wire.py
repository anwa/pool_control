# sensors/one_wire.py
import os
from utils.config import config
from w1thermsensor import W1ThermSensor, SensorNotReadyError

class OneWireReader:
    def __init__(self):
        self.id_to_name = config.get_onewire_mapping()
        self.ignored = config.load_ignored()
        self.available_sensors = {s.id: s for s in W1ThermSensor.get_available_sensors()}

        # Entferne gefundene Sensoren aus ignore-Liste
        found_and_ignored = set(self.ignored) & set(self.available_sensors.keys())
        if found_and_ignored:
            print(f"found_and_ignored: {found_and_ignored}")
            for sensor_id in found_and_ignored:
                config.remove_ignored_sensor(sensor_id)
                self.ignored.discard(sensor_id)

    """
    def load_ignored(self):
        try:
            if not config.config.has_section("1-Wire-Ignore"):
                return set()
            return set(config.config.options("1-Wire-Ignore"))
        except Exception as e:
            print(f"Fehler beim Laden ignorierter Sensoren: {e}")
            return set()
    """

    def remove_ignored_sensor(self, sensor_id):
        if config.config.has_option("1-Wire-Ignore", sensor_id):
            config.config.remove_option("1-Wire-Ignore", sensor_id)
            with open("config.ini", "w") as configfile:
                config.config.write(configfile)
        self.ignored.discard(sensor_id)

    def get_missing_sensors(self):
        missing = []
        for sensor_id in self.id_to_name:
            if sensor_id not in self.available_sensors and sensor_id not in self.ignored:
                missing.append(sensor_id)
        return missing

    def ignore_sensor(self, sensor_id):
        try:
            if sensor_id not in self.ignored:
                self.ignored.add(sensor_id)
                config.ignore_sensor_permanently(sensor_id)
        except Exception as e:
            print(f"Fehler beim Speichern ignorierter Sensoren: {e}")

    """ 
    def read_all(self):
        results = {}
        for sensor_id, name in self.id_to_name.items():
            if sensor_id in self.ignored:
                continue
            sensor = self.available_sensors.get(sensor_id)
            if sensor is None:
                results[name] = None
                continue
            try:
                temp_c = round(sensor.get_temperature(), 2)
                results[name] = temp_c
            except SensorNotReadyError:
                results[name] = None
        return results
    """