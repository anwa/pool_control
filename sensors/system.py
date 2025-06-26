from utils.logger import logger
import os

def read_cpu_temperature():
    try:
        with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
            temp_milli = int(f.read().strip())
        temp_celsius = temp_milli / 1000.0
        logger.debug(f"CPU-Temperatur: {temp_celsius:.1f} °C")
        return temp_celsius
    except Exception as e:
        logger.error(f"Fehler beim Auslesen der CPU-Temperatur: {e}")
        return "n.a."
