from utils.logger import logger
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.clock import Clock
from datetime import datetime
from utils.network import get_ip, get_wifi_strength


class MainScreen(BoxLayout):
    date_time = StringProperty()
    ip_address = StringProperty()
    wifi_strength = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.update_time(0)
        self.date_time = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        self.ip_address = get_ip()
        self.wifi_strength = str(get_wifi_strength())

        # Zeit jede Sekunde aktualisieren
        Clock.schedule_interval(self.update_time, 1)
        # IP alle 10 Minuten (600 Sekunden) aktualisieren
        Clock.schedule_interval(self.update_ip, 600)
        # WLAN alle 30 Sekunden aktualisieren
        Clock.schedule_interval(self.update_wifi, 30)

    def update_time(self, dt):
        self.date_time = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

    def update_ip(self, dt):
        self.ip_address = get_ip()

    def update_wifi(self, dt):
        self.wifi_strength = str(get_wifi_strength())
