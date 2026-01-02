[app]
# =========================
# App identity
# =========================
title = Wildlife Pro Studio
package.name = wildlifepro
package.domain = org.wildlifepro
version = 1.0

# =========================
# Source configuration
# =========================
source.dir = .
source.include_exts = py,kv,png,jpg,jpeg,atlas,mp3,wav,ogg,flac

# =========================
# UI / display
# =========================
orientation = portrait
fullscreen = 0

# =========================
# Python requirements
# =========================
# IMPORTANT:
# - pyjnius (NOT jnius)
# - kivymd pinned to stable 1.1.1
# - NO ffmpeg recipe (you use libffmpeg.so manually)
requirements = python3,kivy==2.3.0,kivymd==1.1.1,pillow,android,pyjnius,pydub

# =========================
# Android permissions
# =========================
# Android 13+ compatible
android.permissions = INTERNET,READ_MEDIA_AUDIO

# =========================
# Android SDK / NDK
# =========================
# CRITICAL: API 33 is stable
android.api = 33
android.minapi = 21
android.ndk = 25b

# CRITICAL: This fixes AIDL errors
android.build_tools = 33.0.2

# =========================
# Architecture
# =========================
# 64-bit only (Play Store compliant)
android.archs = arm64-v8a

# =========================
# Native libraries
# =========================
# Your manually supplied FFmpeg binary
android.add_libs = libffmpeg.so

# =========================
# Android options
# =========================
android.enable_androidx = True
android.private_storage = True
android.allow_backup = True

# =========================
# Buildozer settings
# =========================
[buildozer]
log_level = 2
warn_on_root = 1
