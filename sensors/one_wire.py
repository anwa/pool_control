# sensors/one_wire.py
import os
from utils.config import config
from w1thermsensor import W1ThermSensor, SensorNotReadyError

IGNORED_FILE = "ignored_sensors.txt"

class OneWireReader:
    def __init__(self):
        self.id_to_name = config.get_onewire_mapping()
        self.ignored = self.load_ignored()
        self.available_sensors = {s.id: s for s in W1ThermSensor.get_available_sensors()}
        # self.sensors = W1ThermSensor.get_available_sensors()

    def load_ignored(self):
        if os.path.exists(IGNORED_FILE):
            with open(IGNORED_FILE, "r") as f:
                return set(line.strip() for line in f if line.strip())
        return set()

    def save_ignored(self):
        with open(IGNORED_FILE, "w") as f:
            f.write("\n".join(self.ignored))

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