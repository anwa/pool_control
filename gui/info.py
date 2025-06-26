from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, BooleanProperty
from kivy.lang import Builder
from kivy.clock import Clock
from sensors.system import read_cpu_temperature

Builder.load_file("gui/info.kv")


class InfoPage(BoxLayout):
    cpu_temp = StringProperty("0")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cpu_temp = str(read_cpu_temperature())

        # alle 10 Sekunden aktualisieren
        Clock.schedule_interval(self.update, 10)

    def update(self, dt):
        self.cpu_temp = str(read_cpu_temperature())

