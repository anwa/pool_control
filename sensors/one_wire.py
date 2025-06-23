from w1thermsensor import W1ThermSensor


class OneWireSensors:
    def __init__(self):
        self.sensors = W1ThermSensor.get_available_sensors()

    def read_all(self):
        return {sensor.id: sensor.get_temperature() for sensor in self.sensors}
