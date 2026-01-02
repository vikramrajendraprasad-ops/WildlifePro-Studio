
import os
import sys
import shutil
import threading
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

# Import Android-specific permissions and classes safely
if platform == 'android':
    from android.permissions import request_permissions, Permission
    from jnius import autoclass

class WildlifeStudio(MDApp):
    selected_format = "mp3"
    selected_channels = "2"
    channel_map = {"Mono": 1, "Stereo": 2, "5.1": 6}

    def build(self):
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.theme_style = "Dark"
        
        screen = MDScreen()
        layout = MDBoxLayout(orientation='vertical')

        # Toolbar
        toolbar = MDTopAppBar(
            title="Wildlife Pro Studio", 
            elevation=4,
            right_action_items=[["refresh", lambda x: self.load_files()]]
        )
        layout.add_widget(toolbar)

        # Settings Area
        settings = MDBoxLayout(size_hint_y=None, height="60dp", padding=10, spacing=10)
        self.btn_format = MDRaisedButton(text="MP3", on_release=lambda x: self.menu_format.open())
        self.btn_channels = MDRaisedButton(text="Stereo", on_release=lambda x: self.menu_channels.open())
        settings.add_widget(self.btn_format)
        settings.add_widget(self.btn_channels)
        layout.add_widget(settings)

        # File List Area
        self.scroll = MDScrollView()
        self.list_view = MDList()
        self.scroll.add_widget(self.list_view)
        layout.add_widget(self.scroll)

        # Status/Action Bar
        self.status = MDRaisedButton(
            text="Initializing...", 
            size_hint_x=1, 
            disabled=True
        )
        layout.add_widget(self.status)
        
        screen.add_widget(layout)
        self.create_menus()
        return screen

    def create_menus(self):
        self.menu_format = MDDropdownMenu(
            caller=self.btn_format, 
            items=[{"text": f.upper(), "viewclass": "OneLineListItem", "on_release": lambda x=f: self.set_format(x)} for f in ["mp3", "wav", "flac"]], 
            width_mult=4
        )
        self.menu_channels = MDDropdownMenu(
            caller=self.btn_channels, 
            items=[{"text": k, "viewclass": "OneLineListItem", "on_release": lambda x=k: self.set_channels(x)} for k in self.channel_map], 
            width_mult=4
        )

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
            self.configure_ffmpeg_android()
            self.request_android_permissions()
        else:
            self.status.text = "Desktop Mode"
            self.load_files()

    def request_android_permissions(self):
        """
        Request permissions compatible with Android 13+ (API 33) and older versions.
        """
        try:
            from android import api_version
            permissions = []
            
            # API 33+ (Android 13) requires granular media permissions
            if api_version >= 33:
                permissions.append(Permission.READ_MEDIA_AUDIO)
                # permissions.append(Permission.READ_MEDIA_IMAGES) # If you handle images
            else:
                # Older Android versions
                permissions.append(Permission.READ_EXTERNAL_STORAGE)
                permissions.append(Permission.WRITE_EXTERNAL_STORAGE)

            request_permissions(permissions, self.on_permissions_result)
        except Exception as e:
            self.status.text = f"Perm Error: {str(e)}"

    def on_permissions_result(self, permissions, grants):
        # We try to load files regardless of result, just in case
        Clock.schedule_once(lambda dt: self.load_files(), 0.5)

    def configure_ffmpeg_android(self):
        """
        CRITICAL: Locates the libffmpeg.so library packaged by Buildozer
        and tells Pydub to use it as the converter executable.
        """
        try:
            from pydub import AudioSegment
            
            # Get the path where Android extracts native libraries (.so files)
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            context = PythonActivity.mActivity.getApplicationContext()
            lib_path = context.getApplicationInfo().nativeLibraryDir
            
            # The file is named 'libffmpeg.so' because we renamed it in buildozer.spec
            # or it was built as a shared library.
            ffmpeg_binary = os.path.join(lib_path, "libffmpeg.so")
            
            if os.path.exists(ffmpeg_binary):
                AudioSegment.converter = ffmpeg_binary
                # Verify execution permission (usually handled by Android automatically for libs)
                try:
                    os.chmod(ffmpeg_binary, 0o755)
                except:
                    pass
                self.status.text = "FFmpeg Engine Loaded"
            else:
                self.status.text = "FFmpeg binary NOT found in native libs!"
                
        except Exception as e:
            self.status.text = f"Engine Error: {str(e)}"

    def load_files(self, *args):
        self.list_view.clear_widgets()
        # Fallback path for testing - In production consider using android.storage path
        path = "/storage/emulated/0/Download/Wildlife"
        
        try:
            if not os.path.exists(path):
                os.makedirs(path, exist_ok=True)
                
            exts = ['.mp3', '.wav', '.m4a', '.flac', '.ogg']
            files = [f for f in os.listdir(path) if any(f.lower().endswith(e) for e in exts)]
            
            self.status.text = f"Found {len(files)} files"
            
            for f in files:
                item = OneLineIconListItem(
                    text=f, 
                    on_release=lambda x, f_path=os.path.join(path, f): self.convert(f_path)
                )
                item.add_widget(IconLeftWidget(icon="music"))
                self.list_view.add_widget(item)
                
        except PermissionError:
            self.status.text = "Permission Denied! Check Settings."
            toast("Grant Storage Permission manually in Settings")
        except Exception as e:
            self.status.text = f"Error: {str(e)}"

    def convert(self, input_path):
        self.status.text = "Converting..."
        threading.Thread(target=self.process_audio, args=(input_path,)).start()

    def process_audio(self, input_path):
        try:
            from pydub import AudioSegment
            
            # Load
            audio = AudioSegment.from_file(input_path)
            
            # Processing (Bass Boost Example)
            # LowShelf filter is better for bass boost than simple addition
            audio = audio.low_pass_filter(120) + 4 
            
            # Set Format
            channels = int(self.selected_channels)
            audio = audio.set_channels(channels).set_frame_rate(48000)
            
            # Export
            base = os.path.splitext(input_path)[0]
            output_file = f"{base}_Pro.{self.selected_format}"
            
            audio.export(output_file, format=self.selected_format)
            
            # Update UI on Main Thread
            def on_success(dt):
                self.status.text = "Ready"
                toast(f"Saved: {os.path.basename(output_file)}")
                self.load_files()
                
            Clock.schedule_once(on_success)
            
        except Exception as e:
            error_msg = str(e)
            def on_fail(dt):
                self.status.text = "Failed"
                # Show partial error for debugging
                toast(f"Error: {error_msg[:30]}...")
                print(f"CONVERSION ERROR: {error_msg}")
                
            Clock.schedule_once(on_fail)

if __name__ == '__main__':
    WildlifeStudio().run()
