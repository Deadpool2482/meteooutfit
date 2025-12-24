[app]
title = Meteo Outfit
package.name = meteooutfit
package.domain = org.meteo
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 3.1

# Requisiti aggiornati e stabili
requirements = python3,kivy==2.3.0,kivymd,requests,certifi,urllib3,idna,chardet,pillow

orientation = portrait
fullscreen = 0
android.archs = arm64-v8a
android.api = 34
android.minapi = 21
android.ndk = 25b
android.enable_androidx = True
android.permissions = INTERNET, ACCESS_FINE_LOCATION

# ⚠️ ICONA DISATTIVATA per evitare l'errore "File Not Found"
# Togli il # solo dopo aver caricato il file icon.png su GitHub
# icon.filename = %(source.dir)s/icon.png

[buildozer]
log_level = 2
warn_on_root = 1
