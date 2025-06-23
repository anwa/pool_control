import bme280
import smbus2


class BME280Sensor:
    def __init__(self, address=0x76, bus=1):
        self.address = address
        self.bus = smbus2.SMBus(bus)
        self.calibration_params = bme280.load_calibration_params(self.bus, self.address)

    def read(self):
        data = bme280.sample(self.bus, self.address, self.calibration_params)
        return {
            "temperature": data.temperature,
            "humidity": data.humidity,
            "pressure": data.pressure,
        }
