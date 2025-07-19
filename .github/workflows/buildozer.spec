[app]

# App details
title = GhostCore AI
package.name = ghostcoreai
package.domain = org.ghostcore
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0

# Main script
entrypoint = main.py

# Orientation & icon
orientation = portrait
icon.filename = icon.png

# Permissions (for camera, internet, etc.)
android.permissions = INTERNET

# Android SDK settings
android.api = 31
android.minapi = 21
android.ndk = 23b
android.sdk = 24.4.1
android.ndk_path = 
android.sdk_path = 
android.archs = armeabi-v7a,arm64-v8a

# (Optional) If using OpenCV:
# requirements = kivy,opencv-python,numpy
requirements = kivy

# Bootstrap and Java options
android.bootstrap = sdl2
android.entrypoint = org.kivy.android.PythonActivity
android.logcat_filters = *:S python:D

# Whether to copy the apk to the bin directory
copy_to_bin = true
