from utils.logger import logger
import psutil
import os
import subprocess

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

def read_cpu_usage(self):
    try:
        usage = psutil.cpu_percent(interval=1)
        logger.debug(f"CPU-Auslastung: {usage:.1f}%")
        return usage
    except Exception as e:
        logger.error(f"Fehler beim Auslesen der CPU-Auslastung: {e}")
        return "n.a."

def read_memory_usage(self):
    try:
        mem = psutil.virtual_memory()
        usage_percent = mem.percent
        logger.debug(f"RAM-Nutzung: {usage_percent:.1f}%")
        return usage_percent
    except Exception as e:
        logger.error(f"Fehler beim Auslesen der RAM-Nutzung: {e}")
        return "n.a."

def read_sd_card_usage(self):
    try:
        result = subprocess.check_output(["df", "-h", "/"]).decode()
        for line in result.splitlines():
            if "/dev/root" in line or "/" in line:
                usage_percent = float(line.split()[4].rstrip("%"))
                logger.debug(f"SD-Karten-Nutzung: {usage_percent:.1f}%")
                return usage_percent
        logger.warning("Keine SD-Karten-Informationen gefunden")
        return "n.a."
    except Exception as e:
        logger.error(f"Fehler beim Auslesen der SD-Karten-Nutzung: {e}")
        return "n.a."
