from kivy.uix.boxlayout import BoxLayout
from utils.config import config
from kivy.lang import Builder
from kivy.properties import StringProperty, BooleanProperty

Builder.load_file("gui/messung.kv")


class MessungPage(BoxLayout):
    # Properties für Messwerte
    ph_value = StringProperty("7.2")
    pool_temp = StringProperty("24.5 °C")
    tds_value = StringProperty("800 ppm")
    pool_power = StringProperty("2975 W")
    pool_energy_today = StringProperty("11.30 kWh")
    pool_energy_yesterday = StringProperty("21.65 kWh")
    wp_current_temp = StringProperty("")
    wp_target_temp = StringProperty("")
    pass
