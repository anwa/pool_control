import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn


class ADS1115Sensor:
    def __init__(self, channel=0):
        i2c = busio.I2C(board.SCL, board.SDA)
        self.ads = ADS.ADS1115(i2c)
        self.channel = AnalogIn(self.ads, getattr(ADS, f"P{channel}"))

    def read(self):
        return self.channel.voltage
