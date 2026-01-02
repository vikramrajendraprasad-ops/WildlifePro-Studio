[app]
title = Locked SDK App
package.name = lockedsdk
package.domain = org.locked
version = 0.1

source.dir = .
source.include_exts = py

requirements = python3,kivy

orientation = portrait
fullscreen = 0

# 🔒 MUST MATCH WORKFLOW SDK
android.api = 33
android.minapi = 21
android.ndk = 25b
android.build_tools = 33.0.2
android.archs = arm64-v8a

android.permissions = INTERNET

[buildozer]
log_level = 2
warn_on_root = 1
