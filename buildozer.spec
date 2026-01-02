
[app]
title = Wildlife Pro Studio
package.name = wildlifepro
package.domain = org.wildlifepro

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 2.0

# FIXED VERSIONS - Guaranteed to compile
requirements = python3,kivy==2.1.0,kivymd==1.1.1,pillow,pydub

orientation = portrait
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,MANAGE_EXTERNAL_STORAGE

# FIXED NDK (matches GitHub Actions)
android.ndk = 25b
android.api = 33
android.minapi = 21
android.archs = arm64-v8a
android.accept_sdk_license = True

[buildozer]
log_level = 2
