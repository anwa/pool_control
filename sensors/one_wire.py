# sensors/one_wire.py
import os
from utils.config import config
from w1thermsensor import W1ThermSensor, SensorNotReadyError

class OneWireReader:
    def __init__(self):
        self.id_to_name = config.get_onewire_mapping()
        self.ignored = config.get_ignored_sensors()
        self.available_sensors = {s.id: s for s in W1ThermSensor.get_available_sensors()}

        # Entferne gefundene Sensoren aus ignore-Liste
        found_and_ignored = set(self.ignored) & set(self.available_sensors.keys())
        if found_and_ignored:
            print(f"found_and_ignored: {found_and_ignored}")
            self.ignored -= found_and_ignored
            config.set_ignored_sensors(self.ignored)

    def load_ignored(self):
        try:
            ignored_str = config.get("1-Wire", "ignored", fallback="")
            return set(s.strip() for s in ignored_str.split(",") if s.strip())
        except Exception as e:
            print(f"Fehler beim Laden ignorierter Sensoren: {e}")
            return set()

    def save_ignored(self):
        try:
            ignored_str = ", ".join(sorted(self.ignored))
            config.set("1-Wire", "ignored", ignored_str)
        except Exception as e:
            print(f"Fehler beim Speichern ignorierter Sensoren: {e}")

    def get_missing_sensors(self):
        missing = []
        for sensor_id in self.id_to_name:
            if sensor_id not in self.available_sensors and sensor_id not in self.ignored:
                missing.append(sensor_id)
        return missing

    def ignore_sensor(self, sensor_id):
        self.ignored.add(sensor_id)
        self.save_ignored()

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