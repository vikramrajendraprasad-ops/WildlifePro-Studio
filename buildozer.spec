[app]
# App details
title = Wildlife Pro Studio
package.name = wildlifepro
package.domain = org.wildlifepro

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,mp3,wav,flac,ogg

version = 2.0

# PyDub Requirements (NO FFmpeg binary!)
requirements = python3,kivy==2.3.0,kivymd==2.0.0,pillow,pydub,android

# UI Settings
orientation = portrait
fullscreen = 0

# Android 12+ Permissions (Fixed for Poco X3)
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,MANAGE_EXTERNAL_STORAGE,WAKE_LOCK

# Android Build Config
android.api = 33
android.minapi = 21
android.ndk = 26b
android.archs = arm64-v8a
android.accept_sdk_license = True
android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 0
