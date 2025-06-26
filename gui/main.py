from utils.logger import logger
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.clock import Clock
from datetime import datetime
from utils.network import get_ip, get_wifi_strength
from gui.info import InfoPage
from gui.messung import MessungPage
from gui.settings import SettingsPage
from gui.relays import RelaysView


class MainScreen(BoxLayout):
    # Properties für Kopfbereich
    date_time = StringProperty()
    # Properties für Fußbereich
    ip_address = StringProperty("192.168.1.100")
    wifi_strength = StringProperty("-60 dBm")

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
        Clock.schedule_interval(self.update_wifi, 10)
        # Lade InfoPage beim Start
        Clock.schedule_once(self.show_info, 0)
        # Nach 5 Sekunden auf Messung wechseln
        Clock.schedule_once(self.show_messung, 5)

    def update_time(self, dt):
        self.date_time = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

    def update_ip(self, dt):
        self.ip_address = get_ip()

    def update_wifi(self, dt):
        self.wifi_strength = str(get_wifi_strength())

    def show_page(self, page_name):
        # Hier kannst du die Seitenumschaltung implementieren
        logger.info(f"Seite wechseln zu: {page_name}")
        center_area = self.ids.center_area
        right_area = self.ids.right_area
        center_area.clear_widgets()
        right_area.clear_widgets()
        if page_name == "main":
            center_area.add_widget(MessungPage())
            right_area.add_widget(RelaysView())
        elif page_name == "settings":
            center_area.add_widget(SettingsPage())
        elif page_name == "info":
            center_area.add_widget(InfoPage())

    def show_info(self, dt):
        self.show_page("info")

    def show_messung(self, dt):
        self.show_page("main")
