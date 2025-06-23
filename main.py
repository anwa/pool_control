from utils.logger import logger

# from kivy.config import Config
# Config.set('graphics', 'fullscreen', 'auto')

from kivy.lang import Builder

Builder.load_file("gui/main.kv")

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from gui.main import MainScreen


class PoolControlApp(App):
    def build(self):
        logger.info("Application started.")
        self.title = "Pool Control"
        self.icon = "gui/icons/pool.png"
        self.root = MainScreen()
        Clock.schedule_interval(self.root.update_time, 1)
        return self.root

    def on_stop(self):
        logger.info("Application stopped.")


if __name__ == "__main__":
    PoolControlApp().run()
