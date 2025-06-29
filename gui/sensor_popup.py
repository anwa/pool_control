from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import Spinner
from kivy.uix.label import Label
from kivy.uix.button import Button


def show_missing_sensors_popup(missing_ids, reader, on_done):
    layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

    for sensor_id in missing_ids:
        label = Label(text=f"Sensor {sensor_id} fehlt.")
        btn_ignore = Button(text="Ignorieren")
        btn_delete = Button(text="Löschen aus Config")
        btn_keep = Button(text="Behalten")

        def make_callback(action, sid=sensor_id):
            def callback(instance):
                if action == "ignore":
                    reader.ignore_sensor(sid)
                elif action == "delete":
                    reader.remove_ignored_sensor(sid)
                    reader.id_to_name.pop(sid, None)
                popup.dismiss()
                on_done()
            return callback

        btn_ignore.bind(on_press=make_callback("ignore"))
        btn_delete.bind(on_press=make_callback("delete"))
        btn_keep.bind(on_press=make_callback("keep"))

        layout.add_widget(label)
        layout.add_widget(btn_ignore)
        layout.add_widget(btn_delete)
        layout.add_widget(btn_keep)

    popup = Popup(title="Fehlende Sensoren", content=layout, size_hint=(0.8, 0.8))
    popup.open()


def show_new_sensor_popup(sensor_infos, reader, on_done):
    layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

    # Verfügbare Namen
    used_names = set(reader.id_to_name.values())
    all_names = ["Pool", "PH_IN", "PH_OUT", "WP_OUT"]
    free_names = [n for n in all_names if n not in used_names]

    assignments = {}

    for sensor_id, temp in sensor_infos:
        temp_display = f"{temp} °C" if temp is not None else "?"
        label = Label(text=f"{sensor_id} - {temp_display}")
        spinner = Spinner(text="Name wählen", values=free_names)

        def on_select(spinner, text, sid=sensor_id):
            assignments[sid] = text

        spinner.bind(text=on_select)
        layout.add_widget(label)
        layout.add_widget(spinner)

    def on_confirm(instance):
        for sid, name in assignments.items():
            if name != "Name wählen":
                reader.assign_name(sid, name)
        popup.dismiss()
        on_done()

    confirm_btn = Button(text="Speichern und fortfahren")
    confirm_btn.bind(on_press=on_confirm)
    layout.add_widget(confirm_btn)

    popup = Popup(title="Neue Sensoren erkannt", content=layout, size_hint=(0.9, 0.9))
    popup.open()
