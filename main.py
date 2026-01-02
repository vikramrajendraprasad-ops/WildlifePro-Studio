
from kivy.app import App
from kivy.uix.label import Label

class TestApp(App):
    def build(self):
        return Label(text="SDK LOCKED ✅", font_size="24sp")

if __name__ == "__main__":
    TestApp().run()
