import logging
from logging.handlers import TimedRotatingFileHandler
import os
import gzip
import shutil
from utils.config import config

class GZipTimedRotatingFileHandler(TimedRotatingFileHandler):
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

log_dir = config.get('Log', 'dir', fallback='./logs')
retention_days = config.getint('Log', 'retention_days', fallback=7)
log_level_str = config.get('Log', 'level', fallback='INFO').upper()
log_level = getattr(logging, log_level_str, logging.INFO)

os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "poolcontrol.log")

# Rotierender Handler: täglich neue Datei, max. N Backups
rotating_handler = GZipTimedRotatingFileHandler(
    log_file,
    when="midnight",
    interval=1,
    backupCount=retention_days,
    encoding="utf-8",
    utc=False  # Stelle ggf. auf True um, wenn du UTC willst
)
rotating_handler.suffix = "%Y-%m-%d"

logging.basicConfig(
    level=log_level,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[rotating_handler, logging.StreamHandler()],
)
logger = logging.getLogger("PoolControl")
