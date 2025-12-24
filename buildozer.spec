[app]
# Nome che apparirà sotto l'icona sul telefono
title = Meteo Outfit

# Identificativo univoco dell'app
package.name = meteooutfit
package.domain = org.meteo

# Dove si trova il codice (cartella corrente)
source.dir = .

# Estensioni dei file da includere (importante che ci sia 'png')
source.include_exts = py,png,jpg,kv,atlas

# Versione dell'app
version = 2.5

# Requisiti: HO INCLUSO PILLOW PER GESTIRE L'ICONA E LE IMMAGINI
requirements = python3,kivy==2.3.0,kivymd,requests,certifi,urllib3,idna,chardet,pillow

# Orientamento schermo (verticale)
orientation = portrait
fullscreen = 0

# --- CONFIGURAZIONE ICONA ---
# Questa è la riga che attiva la tua icona 'icon.png'
icon.filename = %(source.dir)s/icon.png

# --- CONFIGURAZIONE ANDROID ---
# Architettura standard per telefoni moderni
android.archs = arm64-v8a

# Versioni Android (API 34 = Android 14)
android.api = 34
android.minapi = 21
android.ndk = 25b

# Abilita le librerie moderne
android.enable_androidx = True

# Permessi richiesti
android.permissions = INTERNET, ACCESS_FINE_LOCATION, FOREGROUND_SERVICE

[buildozer]
# Livello di dettaglio dei log (utile per il debug)
log_level = 2
warn_on_root = 1
