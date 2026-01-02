[app]
# Basic app info
title = Wildlife Pro Studio
package.name = wildlifepro
package.domain = org.wildlifepro

# Source files
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,mp3,wav,flac

# Version
version = 2.0

# FIXED Requirements (compiles on GitHub Actions)
requirements = python3,kivy==2.1.0,kivymd==1.1.1,pillow,pydub

# UI settings
orientation = portrait
fullscreen = 0
presplash.filename = %(source.dir)s/icon.png

# Permissions (Android 12+)
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,MANAGE_EXTERNAL_STORAGE,WAKE_LOCK

# Android build config (FIXED NDK)
android.api = 33
android.minapi = 21
android.ndk = 25b
android.sdk = 33
android.archs = arm64-v8a
android.accept_sdk_license = True
android.add_src_to_manifest = True

# Icon (optional)
android.icon.filename = %(source.dir)s/icon.png

[buildozer]
log_level = 2
warn_on_root = 0
