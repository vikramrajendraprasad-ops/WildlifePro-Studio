import os, threading, subprocess, shutil
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
    from jnius import autoclass, cast

class WildlifeStudio(MDApp):
    ffmpeg_path = "ffmpeg"
    selected_format = "mp3"
    selected_channels = "2"
    channel_map = {"Mono": "1", "Stereo": "2", "5.1": "6", "7.1": "8"}

    def build(self):
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.theme_style = "Dark"
        screen = MDScreen()
        layout = MDBoxLayout(orientation='vertical')

        toolbar = MDTopAppBar(title="Wildlife Pro Studio", right_action_items=[["refresh", lambda x: self.load_files()]])
        layout.add_widget(toolbar)

        settings = MDBoxLayout(orientation='horizontal', size_hint_y=None, height="60dp", padding=10)
        self.btn_format = MDRaisedButton(text="MP3", on_release=self.open_format_menu)
        self.btn_channels = MDRaisedButton(text="Stereo", on_release=self.open_channel_menu)
        settings.add_widget(self.btn_format)
        settings.add_widget(self.btn_channels)
        layout.add_widget(settings)

        scroll = MDScrollView()
        self.list_view = MDList()
        scroll.add_widget(self.list_view)
        layout.add_widget(scroll)

        self.status_btn = MDRaisedButton(text="Ready", disabled=True)
        layout.add_widget(self.status_btn)
        screen.add_widget(layout)
        self.create_menus()
        return screen

    def create_menus(self):
        self.menu_format = MDDropdownMenu(self.btn_format, [{"text": f, "on_release": lambda x=f: setattr(self, 'selected_format', x) or setattr(self.btn_format, 'text', x.upper())} for f in ["mp3","aac","ac3","wav"]], width_mult=4)
        self.menu_channels = MDDropdownMenu(self.btn_channels, [{"text": k, "on_release": lambda x=k: setattr(self, 'selected_channels', self.channel_map[k]) or setattr(self.btn_channels, 'text', k)} for k in self.channel_map], width_mult=4)

    def open_format_menu(self, obj): self.menu_format.open()
    def open_channel_menu(self, obj): self.menu_channels.open()

    def on_start(self):
        if platform == 'android':
            self.setup_ffmpeg()
            self.check_permissions()
        self.load_files()

    def setup_ffmpeg(self):
        self.ffmpeg_path = os.path.join(self.user_data_dir, 'ffmpeg')
        if not os.path.exists(self.ffmpeg_path):
            from kivy.resources import resource_find
            source = resource_find('ffmpeg')
            if source: shutil.copy(source, self.ffmpeg_path); os.chmod(self.ffmpeg_path, 0o755)

    def check_permissions(self, *args):
        if platform == 'android':
            request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE], self.load_files)
            Environment = autoclass("android.os.Environment")
            if not Environment.isExternalStorageManager():
                Settings = autoclass("android.provider.Settings")
                Intent = autoclass("android.content.Intent")
                Uri = autoclass("android.net.Uri")
                intent = Intent(Settings.ACTION_MANAGE_APP_ALL_FILES_ACCESS_PERMISSION, Uri.parse("package:org.wildlifepro.wildlifepro"))
                autoclass("org.kivy.android.PythonActivity").mActivity.startActivity(intent)

    def load_files(self, *args):
        self.list_view.clear_widgets()
        path = "/storage/emulated/0/Download/Wildlife"
        os.makedirs(path, exist_ok=True)
        exts = '.mp3 .wav .m4a .flac .ogg .aac .ac3'.split()
        files = [f for f in os.listdir(path) if any(f.lower().endswith(e) for e in exts)]
        if files:
            self.status_btn.text = f"{len(files)} files"
            for f in files:
                item = OneLineIconListItem(text=f, on_release=lambda x, p=os.path.join(path,f): self.process_audio(p))
                item.add_widget(IconLeftWidget(icon="music"))
                self.list_view.add_widget(item)
        else:
            self.status_btn.text = "No files"

    def process_audio(self, path):
        self.status_btn.text = "Converting..."
        threading.Thread(target=self.convert, args=(path,)).start()

    def convert(self, input_path):
        try:
            base = os.path.splitext(input_path)[0]
            output = f"{base}_Pro.{self.selected_format}"
            cmd = [self.ffmpeg_path, '-y', '-i', input_path, '-ac', self.selected_channels, '-af', 'equalizer=f=60:g=5', output]
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            p.communicate()
            if p.returncode == 0:
                Clock.schedule_once(lambda x: (self.status_btn.text.__setitem__('text', 'Success!'), toast(f"✅ {os.path.basename(output)}")))
            else:
                Clock.schedule_once(lambda x: self.status_btn.text.__setitem__('text', 'Error'))
        except Exception as e:
            Clock.schedule_once(lambda x: self.status_btn.text.__setitem__('text', f"Error: {e}"))

WildlifeStudio().run()
