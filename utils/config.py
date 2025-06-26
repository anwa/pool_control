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
            print(f"Fehler beim Lesen von [{section}] {option}: {e}")
            return fallback

    def set(self, section, option, value):
        self.config.set(section, option, str(value))
        with open("config.ini", "w") as configfile:
            self.config.write(configfile)


# Singleton-Instanz für die Anwendung
config = Config("config.ini")
