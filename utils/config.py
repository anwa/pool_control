#from utils.logger import logger
import configparser
import os


class Config:
    """
    Lädt und speichert die Konfiguration aus einer INI-Datei.
    """

    def __init__(self, filename="config.ini"):
        self.config = configparser.ConfigParser()
        if not os.path.exists(filename):
            raise FileNotFoundError(f"Konfigurationsdatei {filename} nicht gefunden!")
        self.config.read(filename)

    def get(self, section, option, fallback=None, type_cast=str):
        """
        Gibt den Wert aus der Konfiguration zurück, mit optionalem Typ-Cast.
        """
        try:
            value = self.config.get(section, option, fallback=fallback)
            if value is not None and type_cast is not str:
                return type_cast(value)
            return value
        except Exception as e:
            #logger.error(f"Fehler beim Lesen von [{section}] {option}: {e}")
            print(f"Fehler beim Lesen von [{section}] {option}: {e}")
            return fallback

    def get_onewire_mapping(self) -> dict:
        """
        Gibt ein Dictionary der 1-Wire Sensoren aus dem Abschnitt [1-Wire] zurück.
        Format: {sensor_id: name}
        """
        try:
            return dict(self.config.items("1-Wire"))
        except configparser.NoSectionError:
            print("Kein Abschnitt [1-Wire] in der Konfigurationsdatei gefunden.")
            return {}

    def get_sensor_id_by_name(self, name: str) -> str | None:
        """
        Gibt die Sensor-ID für einen gegebenen Namen aus dem Abschnitt [1-Wire] zurück, case-insensitiv.
        """
        try:
            name = name.strip().lower()
            mapping = self.get_onewire_mapping()
            for sensor_id, display_name in mapping.items():
                if display_name.strip().lower() == name:
                    return sensor_id
            print(f"Fehler: Sensor mit Name: '{name}' nicht configuriert!")
            return None
        except Exception as e:
            print(f"Fehler beim Auflösen des Namens '{name}': {e}")
            return None

    def ignore_sensor_permanently(self, sensor_id: str):
        if not self.config.has_section("1-Wire-Ignore"):
            self.config.add_section("1-Wire-Ignore")
        self.config.set("1-Wire-Ignore", sensor_id, "true")
        with open("config.ini", "w") as configfile:
            self.config.write(configfile)

    def is_sensor_ignored(self, sensor_id: str) -> bool:
        return self.config.getboolean("1-Wire-Ignore", sensor_id, fallback=False)

    def get_ignored_sensors(self) -> set[str]:
        """
        Liest die ignorierten Sensoren aus dem Abschnitt [1-Wire], Schlüssel 'ignored'.
        Gibt eine Menge von Sensor-IDs zurück.
        """
        try:
            ignored_str = self.get("1-Wire", "ignored", fallback="")
            return set(s.strip() for s in ignored_str.split(",") if s.strip())
        except Exception as e:
            print(f"Fehler beim Lesen ignorierter Sensoren: {e}")
            return set()

    def set_ignored_sensors(self, sensor_ids: set[str]):
        """
        Speichert die ignorierten Sensoren als kommaseparierte Liste in config.ini.
        """
        try:
            ignored_str = ", ".join(sorted(sensor_ids))
            if not self.config.has_section("1-Wire"):
                self.config.add_section("1-Wire")
            self.set("1-Wire", "ignored", ignored_str)
        except Exception as e:
            print(f"Fehler beim Speichern ignorierter Sensoren: {e}")

    def delete_sensor(self, sensor_id: str):
        if self.config.has_option("1-Wire", sensor_id):
            self.config.remove_option("1-Wire", sensor_id)
            with open("config.ini", "w") as configfile:
                self.config.write(configfile)

    def set(self, section, option, value):
        self.config.set(section, option, str(value))
        with open("config.ini", "w") as configfile:
            self.config.write(configfile)


# Singleton-Instanz für die Anwendung
config = Config("config.ini")
