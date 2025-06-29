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
            for sensor_id in found_and_ignored:
                config.remove_ignored_sensor(sensor_id)
                self.ignored.discard(sensor_id)

        # Neue Sensoren: nicht bekannt & nicht ignoriert
        known_ids = set(self.id_to_name.keys()) | self.ignored
        self.new_sensors = [sid for sid in self.available_sensors if sid not in known_ids]

    def read_all(self):
        """
        Liefert ein Dictionary mit allen benannten Sensoren und ihren aktuellen Temperaturen.
        """
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

    def assign_name(self, sensor_id, name):
        config.set("1-Wire", sensor_id, name)
        self.id_to_name[sensor_id] = name
        print(f"id_to_name: {self.id_to_name}")

    def get_new_sensors(self):
        """
        Gibt eine Liste neuer Sensor-IDs zurück (noch nicht bekannt oder ignoriert).
        """
        return self.new_sensors

    def get_new_sensor_info(self):
        """
        Gibt eine Liste von Tupeln (sensor_id, temperatur) für neue Sensoren zurück.
        """
        infos = []
        for sid in self.new_sensors:
            try:
                temp = round(self.available_sensors[sid].get_temperature(), 2)
            except Exception:
                temp = None
            infos.append((sid, temp))
        return infos
    