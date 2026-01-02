[app]
title = Wildlife Pro Studio
package.name = wildlifepro
package.domain = org.wildlifepro
version = 1.0

source.dir = .
source.include_exts = py,kv,png,jpg,atlas,mp3,wav

orientation = portrait
fullscreen = 0

# ✅ STABLE REQUIREMENTS ONLY
requirements = python3,kivy==2.3.0,kivymd==1.1.1,pillow,android,pyjnius,pydub

# Android permissions (Android 13+ compatible)
android.permissions = INTERNET,READ_MEDIA_AUDIO,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE

# Android build configuration
android.api = 34
android.minapi = 21
android.ndk = 25b
android.build_tools = 33.0.2

# Architecture (64-bit required by Play Store)
android.archs = arm64-v8a

# ✅ Bundle your own FFmpeg binary
android.add_libs = libffmpeg.so

android.enable_androidx = True
android.allow_backup = True
android.private_storage = True

[buildozer]
log_level = 2
warn_on_root = 1
