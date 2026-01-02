from kivy.app import App
from kivy.uix.label import Label

class LockedSDKApp(App):
    def build(self):
        return Label(
            text="ANDROID SDK LOCKED ✅",
            font_size="24sp"
        )

if __name__ == "__main__":
    LockedSDKApp().run()
