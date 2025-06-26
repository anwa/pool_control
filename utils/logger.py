import logging
from logging.handlers import TimedRotatingFileHandler
import os
import gzip
import shutil
from utils.config import config

class GZipTimedRotatingFileHandler(TimedRotatingFileHandler):
    """Erweiterter Handler: rotiert tägliche Logdateien und komprimiert sie als .gz"""
    def doRollover(self):
        super().doRollover()

        # Finde das zuletzt rotierte File
        log_dir, base = os.path.split(self.baseFilename)
        for filename in os.listdir(log_dir):
            if filename.startswith(base) and not filename.endswith(".gz"):
                full_path = os.path.join(log_dir, filename)
                if os.path.isfile(full_path) and filename != os.path.basename(self.baseFilename):
                    gz_path = full_path + ".gz"
                    with open(full_path, "rb") as f_in, gzip.open(gz_path, "wb") as f_out:
                        shutil.copyfileobj(f_in, f_out)
                    os.remove(full_path)

# === Konfiguration aus config.ini ===
log_dir = config.get('Log', 'dir', fallback='./logs')
retention_days = int(config.get('Log', 'retention_days', fallback=7))
log_level_str = config.get('Log', 'level', fallback='WARNING').upper() # DEBUG, INFO, WARNING, ERROR, CRITICAL
log_level = getattr(logging, log_level_str, logging.WARNING)

os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "poolcontrol.log")

# === Logger initialisieren ===
logger = logging.getLogger("PoolControl")
logger.setLevel(log_level)  # Wichtig: Logger-Level setzen

# === Rotierender File-Handler mit .gz-Komprimierung ===
file_handler = GZipTimedRotatingFileHandler(
    log_file,
    when="midnight",
    interval=1,
    backupCount=retention_days,
    encoding="utf-8",
    utc=False  # Stelle ggf. auf True um, wenn du UTC willst
)
file_handler.setLevel(log_level)  # Wichtig: Handler-Level setzen
file_handler.suffix = "%Y-%m-%d"
file_formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
file_handler.setFormatter(file_formatter)

# === Konsolen-Handler (für stdout / systemd) ===
console_handler = logging.StreamHandler()
console_handler.setLevel(log_level)
console_handler.setFormatter(file_formatter)

# === Handler registrieren ===
logger.handlers.clear()
logger.addHandler(file_handler)
logger.addHandler(console_handler)