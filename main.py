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

# --- LOGICA DELLE TESSERE ---
class WeatherTile(MDCard):
    def __init__(self, date, temp, weather_emoji, advice, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = "10dp"
        self.elevation = 2
        self.radius = [12, ]
        self.md_bg_color = [1, 1, 1, 1] 
        
        # Data
        self.add_widget(MDLabel(text=date, bold=True, halign="center", font_style="Caption"))
        
        # Temperatura + Emoji Meteo (es: "22°C ☀️")
        self.add_widget(MDLabel(
            text=f"{temp}°C {weather_emoji}", 
            halign="center", 
            font_style="H5", 
            theme_text_color="Primary"
        ))
        
        # Consiglio Outfit
        self.add_widget(MDLabel(
            text=advice, 
            halign="center", 
            font_style="Caption", 
            theme_text_color="Secondary"
        ))

# --- SCHERMATA PRINCIPALE ---
class MeteoScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = MDBoxLayout(orientation='vertical', spacing="10dp")
        
        layout.add_widget(MDTopAppBar(title="Meteo & Outfit"))
        
        self.grid = MDGridLayout(cols=2, spacing="15dp", padding="15dp")
        layout.add_widget(self.grid)
        
        layout.add_widget(MDRaisedButton(
            text="AGGIORNA DATI",
            pos_hint={"center_x": .5},
            on_release=self.start_fetch,
            size_hint=(0.9, None),
            height="50dp"
        ))
        
        layout.add_widget(MDBoxLayout(size_hint_y=None, height="20dp"))
        self.add_widget(layout)

    def get_clothing(self, t):
        if t < 10: return "Cappotto 🧥"
        if t < 18: return "Giacca/Maglione 🧥"
        if t < 25: return "T-shirt e Jeans 👕"
        return "Vestiti Leggeri 😎"

    # Nuova funzione: Converte il codice numerico in Emoji
    def get_weather_emoji(self, code):
        if code == 0: return "☀️" # Sereno
        if code in [1, 2, 3]: return "🌥️" # Nuvoloso
        if code in [45, 48]: return "🌫️" # Nebbia
        if code in [51, 53, 55, 61, 63, 65]: return "🌧️" # Pioggia
        if code in [71, 73, 75]: return "❄️" # Neve
        if code >= 95: return "⛈️" # Temporale
        return "❓"

    def start_fetch(self, *args):
        self.grid.clear_widgets()
        self.grid.add_widget(MDLabel(text="Scaricamento...", halign="center"))
        threading.Thread(target=self.fetch_weather).start()

    def fetch_weather(self):
        # ORA CHIEDIAMO ANCHE 'weathercode'
        url = "https://api.open-meteo.com/v1/forecast?latitude=45.46&longitude=9.18&daily=temperature_2m_max,weathercode&timezone=auto"
        try:
            r = requests.get(url, timeout=10).json()
            daily = r['daily']
            
            # Passiamo tutto alla grafica
            Clock.schedule_once(lambda dt: self.update_ui(daily))
        except Exception as e:
            Clock.schedule_once(lambda dt: self.show_error(str(e)))

    def update_ui(self, daily, *args):
        self.grid.clear_widgets()
        dates = daily['time']
        temps = daily['temperature_2m_max']
        codes = daily['weathercode'] # I codici del meteo (0, 1, 45, ecc)

        for i in range(6):
            day_label = "OGGI" if i == 0 else dates[i][5:]
            emoji = self.get_weather_emoji(codes[i]) # Trasformiamo il codice in emoji
            advice = self.get_clothing(temps[i])
            
            card = WeatherTile(day_label, temps[i], emoji, advice)
            self.grid.add_widget(card)

    def show_error(self, error_msg, *args):
        self.grid.clear_widgets()
        self.grid.add_widget(MDLabel(text="Errore Internet!", halign="center"))

class MeteoApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "DeepPurple" # Ho cambiato colore per festeggiare!
        return MeteoScreen()

if __name__ == "__main__":
    MeteoApp().run()
