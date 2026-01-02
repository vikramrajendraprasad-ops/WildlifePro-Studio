[app]
title = Wildlife Pro Studio
package.name = wildlifepro
package.domain = org.wildlifepro
version = 1.0

source.dir = .
source.include_exts = py,kv,png,jpg,atlas,mp3,wav

orientation = portrait
fullscreen = 0

requirements = python3,kivy==2.3.0,kivymd==1.1.1,pillow,android,pyjnius,pydub

android.permissions = INTERNET,READ_MEDIA_AUDIO

# 🔑 CRITICAL FIX
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a

android.add_libs = libffmpeg.so

[buildozer]
log_level = 2
