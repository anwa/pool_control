# ui/missing_sensor_popup.py
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

class MissingSensorPopup(Popup):
    def __init__(self, sensor_name, sensor_id, callback, **kwargs):
        super().__init__(**kwargs)
        self.title = "Sensor nicht gefunden"
        self.size_hint = (0.8, 0.4)
        self.auto_dismiss = False

        self.sensor_name = sensor_name
        self.sensor_id = sensor_id
        self.callback = callback

        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        label = Label(text=f"Sensor '{sensor_name}' (ID: {sensor_id}) wurde nicht gefunden.\nWas möchten Sie tun?", halign="center")
        label.bind(size=label.setter('text_size'))

        button_layout = BoxLayout(spacing=10, size_hint_y=None, height='40dp')

        btn_ja = Button(text="Ja (Löschen)")
        btn_ja.bind(on_release=lambda instance: self._handle("delete"))

        btn_nein = Button(text="Nein (erneut fragen)")
        btn_nein.bind(on_release=lambda instance: self._handle("keep"))

        btn_ignore = Button(text="Ignorieren")
        btn_ignore.bind(on_release=lambda instance: self._handle("ignore"))

        button_layout.add_widget(btn_ja)
        button_layout.add_widget(btn_nein)
        button_layout.add_widget(btn_ignore)

        layout.add_widget(label)
        layout.add_widget(button_layout)

        self.add_widget(layout)

    def _handle(self, action):
        self.dismiss()
        self.callback(self.sensor_id, action)
