from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty, StringProperty, BooleanProperty
from kivy.lang import Builder
from kivy.clock import Clock
from sensors.system import read_cpu_temperature, read_cpu_usage, read_memory_usage, read_sd_card_usage

Builder.load_file("gui/info.kv")

class InfoPage(BoxLayout):
    cpu_temp = NumericProperty(0.0)
    cpu_use  = NumericProperty(0.0)
    mem_use  = NumericProperty(0.0)
    sd_use   = NumericProperty(0.0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cpu_temp = read_cpu_temperature()
        self.cpu_use = read_cpu_usage()
        self.mem_use = read_memory_usage()
        self.sd_use = read_sd_card_usage()

        # alle 10 Sekunden aktualisieren
        Clock.schedule_interval(self.update, 10)

    def update(self, dt):
        self.cpu_temp = read_cpu_temperature()
        self.cpu_use = read_cpu_usage()
        self.mem_use = read_memory_usage()
        self.sd_use = read_sd_card_usage()

