import socket
import subprocess
from utils.logger import logger


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        logger.info(f"Ermittelte IP-Adresse: {ip}")
    except Exception as e:
        logger.error(f"Fehler beim Ermitteln der IP-Adresse: {e}")
        ip = "N/A"
    finally:
        s.close()
    return ip


def get_wifi_strength():
    try:
        result = subprocess.check_output(["iwconfig", "wlan0"]).decode()
        for line in result.split("\n"):
            if "Link Quality" in line:
                parts = line.strip().split()
                for part in parts:
                    if "Signal" in part:
                        signal = int(part.split("=")[1].replace("dBm", ""))
                        logger.info(f"WLAN Signalstärke: {signal} dBm")
                        return signal
    except Exception as e:
        logger.error(f"Fehler beim Ermitteln der WLAN Signalstärke: {e}")
        return None
    return None
