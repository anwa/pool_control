from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button

class NewSensorPopup(Popup):
    def __init__(self, sensor_id, temperature, available_names, assign_callback, **kwargs):
        super().__init__(title="Neuer 1-Wire Sensor erkannt", size_hint=(0.8, 0.5), **kwargs)
        self.sensor_id = sensor_id
        self.assign_callback = assign_callback

        layout = BoxLayout(orientation="vertical", spacing=10, padding=10)

        layout.add_widget(Label(text=f"Sensor ID: {sensor_id}"))
        layout.add_widget(Label(text=f"Temperatur: {temperature} °C"))

        self.name_spinner = Spinner(
            text="Name wählen",
            values=available_names,
            size_hint=(1, None),
            height=44
        )
        layout.add_widget(self.name_spinner)

        button_layout = BoxLayout(size_hint=(1, None), height=50, spacing=10)
        ok_btn = Button(text="Zuweisen")
        cancel_btn = Button(text="Ignorieren")

        ok_btn.bind(on_release=self._assign_name)
        cancel_btn.bind(on_release=self._ignore_sensor)

        button_layout.add_widget(ok_btn)
        button_layout.add_widget(cancel_btn)
        layout.add_widget(button_layout)

        self.add_widget(layout)

    def _assign_name(self, *args):
        selected = self.name_spinner.text
        if selected != "Name wählen":
            self.assign_callback(self.sensor_id, selected)
            self.dismiss()

    def _ignore_sensor(self, *args):
        self.assign_callback(self.sensor_id, None)
        self.dismiss()
