[app]
title = Wildlife Pro Studio
package.name = wildlifepro
package.domain = org.wildlifepro
version = 1.0

source.dir = .
source.include_exts = py,kv,png,jpg,jpeg,atlas,mp3,wav,ogg,flac

orientation = portrait
fullscreen = 0

# ---- Python requirements ----
# IMPORTANT:
# - pyjnius (NOT jnius)
# - kivymd pinned to stable version
# - ffmpeg NOT included (you use libffmpeg.so manually)
requirements = python3,kivy==2.3.0,kivymd==1.1.1,pillow,android,pyjnius,pydub

# ---- Android permissions ----
android.permissions = INTERNET,READ_MEDIA_AUDIO

# ---- Android SDK / NDK ----
# DO NOT CHANGE THESE
android.api = 33
android.minapi = 21
android.ndk = 25b

# THIS LINE IS THE AIDL FIX
android.build_tools = 33.0.2

# ---- Architecture ----
android.archs = arm64-v8a

# ---- Native libraries ----
# Your custom FFmpeg binary in project root
android.add_libs = libffmpeg.so

android.enable_androidx = True
android.private_storage = True
android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 1
