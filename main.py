from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.toolbar import MDTopAppBar
import requests
import threading
from kivy.clock import Clock

# --- LOGICA DELLE TESSERE GIORNALIERE ---
class WeatherTile(MDCard):
    def __init__(self, date, temp, emoji, advice, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = "10dp"
        self.elevation = 2
        self.radius = [12, ]
        self.md_bg_color = [0.95, 0.95, 0.95, 1]
        
        self.add_widget(MDLabel(text=date, bold=True, halign="center", font_style="Caption"))
        self.add_widget(MDLabel(text=f"{temp}°C {emoji}", halign="center", font_style="H5"))
        self.add_widget(MDLabel(text=advice, halign="center", font_style="Caption", theme_text_color="Secondary"))

# --- SCHERMATA PRINCIPALE ---
class MeteoScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = MDBoxLayout(orientation='vertical')
        
        # Barra superiore
        layout.add_widget(MDTopAppBar(title="Meteo & Outfit Pro"))
        
        # Griglia per i 6 giorni
        self.grid = MDGridLayout(cols=2, spacing="15dp", padding="15dp")
        layout.add_widget(self.grid)
        
        # Pulsante di aggiornamento
        layout.add_widget(MDRaisedButton(
            text="AGGIORNA PREVISIONI",
            pos_hint={"center_x": .5},
            on_release=self.start_fetch,
            size_hint=(0.9, None),
            height="50dp"
        ))
        
        layout.add_widget(MDBoxLayout(size_hint_y=None, height="20dp"))
        self.add_widget(layout)

    def get_weather_info(self, code, t):
        # Determina l'emoji in base al weathercode dell'API
        emoji = "☀️"
        if code in [1, 2, 3]: emoji = "🌥️"
        elif code in [45, 48]: emoji = "🌫️"
        elif code in [51, 53, 55, 61, 63, 65]: emoji = "🌧️"
        elif code >= 95: emoji = "⛈️"
        
        # Consiglio outfit basato sulla temperatura
        advice = "Leggero 😎"
        if t < 12: advice = "Cappotto 🧣"
        elif t < 20: advice = "Giacca 🧥"
        
        return emoji, advice

    def start_fetch(self, *args):
        # Pulisce la griglia e mostra caricamento
        self.grid.clear_widgets()
        self.grid.add_widget(MDLabel(text="Caricamento dati...", halign="center"))
        # Avvia lo scaricamento in un thread separato per non bloccare l'app
        threading.Thread(target=self.fetch_data).start()

    def fetch_data(self):
        # URL API con weathercode e temperature
        url = "https://api.open-meteo.com/v1/forecast?latitude=45.46&longitude=9.18&daily=temperature_2m_max,weathercode&timezone=auto"
        try:
            r = requests.get(url, timeout=10).json()
            # Torna al thread principale per aggiornare l'interfaccia
            Clock.schedule_once(lambda dt: self.update_ui(r['daily']))
        except:
            Clock.schedule_once(lambda dt: self.show_error())

    def update_ui(self, data):
        self.grid.clear_widgets()
        for i in range(6):
            emoji, advice = self.get_weather_info(data['weathercode'][i], data['temperature_2m_max'][i])
            day = "OGGI" if i == 0 else data['time'][i][5:]
            self.grid.add_widget(WeatherTile(day, data['temperature_2m_max'][i], emoji, advice))

    def show_error(self):
        self.grid.clear_widgets()
        self.grid.add_widget(MDLabel(text="Errore di connessione!", halign="center", theme_text_color="Error"))

class MeteoApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Indigo"
        return MeteoScreen()

if __name__ == "__main__":
    MeteoApp().run()
