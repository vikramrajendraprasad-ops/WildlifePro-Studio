
import os, threading
from kivy.utils import platform
from kivy.clock import Clock
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import MDList, OneLineIconListItem, IconLeftWidget
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.menu import MDDropdownMenu
from kivymd.toast import toast

if platform == 'android':
    from android.permissions import request_permissions, Permission
    from jnius import autoclass

class WildlifeStudio(MDApp):
    selected_format = "mp3"
    selected_channels = "2"
    channel_map = {"Mono":1, "Stereo":2, "5.1":6, "7.1":8}

    def build(self):
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.theme_style = "Dark"
        
        screen = MDScreen()
        layout = MDBoxLayout(orientation='vertical')

        # Toolbar
        toolbar = MDTopAppBar(title="Wildlife Pro Studio", right_action_items=[["refresh", lambda x: self.load_files()]])
        layout.add_widget(toolbar)

        # Settings
        settings = MDBoxLayout(size_hint_y=None, height="60dp", padding=10)
        self.btn_format = MDRaisedButton(text="MP3", on_release=lambda x: self.menu_format.open())
        self.btn_channels = MDRaisedButton(text="Stereo", on_release=lambda x: self.menu_channels.open())
        settings.add_widget(self.btn_format)
        settings.add_widget(self.btn_channels)
        layout.add_widget(settings)

        # Files
        self.scroll = MDScrollView()
        self.list_view = MDList()
        self.scroll.add_widget(self.list_view)
        layout.add_widget(self.scroll)

        # Status
        self.status = MDRaisedButton(text="Ready", disabled=True)
        layout.add_widget(self.status)
        
        screen.add_widget(layout)
        self.create_menus()
        return screen

    def create_menus(self):
        self.menu_format = MDDropdownMenu(self.btn_format, [{"text":f.upper(), "on_release": lambda x=f:self.set_format(x)} for f in ["mp3","wav","flac"]], width_mult=4)
        self.menu_channels = MDDropdownMenu(self.btn_channels, [{"text":k, "on_release": lambda x=k:self.set_channels(x)} for k in self.channel_map], width_mult=4)

    def set_format(self, fmt):
        self.selected_format = fmt
        self.btn_format.text = fmt.upper()
        self.menu_format.dismiss()

    def set_channels(self, name):
        self.selected_channels = str(self.channel_map[name])
        self.btn_channels.text = name
        self.menu_channels.dismiss()

    def on_start(self):
        if platform == 'android':
            request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE], self.on_permissions)
            try:
                Settings = autoclass('android.provider.Settings')
                Intent = autoclass('android.content.Intent')
                Uri = autoclass('android.net.Uri')
                intent = Intent(Settings.ACTION_MANAGE_APP_ALL_FILES_ACCESS_PERMISSION, Uri.parse("package:org.wildlifepro.wildlifepro"))
                autoclass('org.kivy.android.PythonActivity').mActivity.startActivity(intent)
            except: pass
        self.load_files()

    def on_permissions(self, *args):
        self.load_files()

    def load_files(self, *args):
        self.list_view.clear_widgets()
        path = "/storage/emulated/0/Download/Wildlife"
        os.makedirs(path, exist_ok=True)
        
        exts = ['.mp3','.wav','.m4a','.flac','.ogg']
        try:
            files = [f for f in os.listdir(path) if any(f.lower().endswith(e) for e in exts)]
        except:
            files = []
            
        self.status.text = f"{len(files)} files" if files else "No files"
        for f in files:
            item = OneLineIconListItem(text=f, on_release=lambda x,f=os.path.join(path,f): self.convert(f))
            item.add_widget(IconLeftWidget(icon="music"))
            self.list_view.add_widget(item)

    def convert(self, input_path):
        self.status.text = "Converting..."
        threading.Thread(target=self.process_audio, args=(input_path,)).start()

    def process_audio(self, input_path):
        try:
            from pydub import AudioSegment
            
            audio = AudioSegment.from_file(input_path)
            audio += 5  # Bass boost
            
            channels = int(self.selected_channels)
            audio = audio.set_channels(channels).set_frame_rate(48000)
            
            base = os.path.splitext(input_path)[0]
            output = f"{base}_Pro.{self.selected_format}"
            audio.export(output, format=self.selected_format)
            
            Clock.schedule_once(lambda dt: (self.status.text.__setitem__('text', 'Success!'), toast(f"✅ {os.path.basename(output)}")))
            Clock.schedule_once(lambda dt: self.load_files(), 1)
            
        except Exception as e:
            Clock.schedule_once(lambda dt: self.status.text.__setitem__('text', f"Error: {e}"))

WildlifeStudio().run()
