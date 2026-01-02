[app]
# Application identity
title = Wildlife Pro Studio
package.name = wildlife_pro_studio
package.domain = org.wildlife
version = 1.0
version.code = 1
source.dir = .

# Application requirements – must include all needed Python modules and libraries
requirements = python3,kivy==2.3.0,kivymd,pillow,pyjnius,pydub,ffmpeg

# Android-specific options
android.permissions = android.permission.READ_EXTERNAL_STORAGE, android.permission.WRITE_EXTERNAL_STORAGE, android.permission.READ_MEDIA_AUDIO, android.permission.READ_MEDIA_VIDEO, android.permission.READ_MEDIA_IMAGES

# Ensure the python-for-android “develop” branch is used (needed for ffmpeg support1)
p4a.branch = develop

# Supported CPU architectures (include 64-bit for Google Play compliance2)
android.archs = arm64-v8a, armeabi-v7a

# Android API levels: target Android 13 (API 33) and allow Android 5.0+ (API 21) as minimum
android.api = 33
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21

orientation = portrait
