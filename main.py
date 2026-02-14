from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

class BusTracker(BoxLayout):
    # ... (garder le code précédent) ...

    def ajouter_arret_manuel(self, nom, heure):
        """ Ajoute un arrêt avec la position GPS actuelle """
        nouvel_arret = {
            "name": nom,
            "lat": self.current_lat,
            "lon": self.current_lon,
            "time": heure
        }
        
        nom_ligne = self.selector.text
        if nom_ligne in self.all_data:
            self.all_data[nom_ligne].append(nouvel_arret)
            self.save_all_data()
            self.status_text = f"Arrêt {nom} ajouté à {nom_ligne}"

    def save_all_data(self):
        """ Sauvegarde permanente dans lignes.json """
        try:
            with open('lignes.json', 'w') as f:
                json.dump(self.all_data, f, indent=4)
        except Exception as e:
            print(f"Erreur sauvegarde : {e}")

    def ouvrir_menu_edition(self):
        """ Crée une petite fenêtre (Popup) pour entrer les infos """
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        nom_input = TextInput(hint_text="Nom de l'arrêt", multiline=False)
        heure_input = TextInput(hint_text="Heure (ex: 12:45)", multiline=False)
        
        btn_valider = Button(text="Enregistrer ici (GPS Actuel)", size_hint_y=None, height=100)
        
        popup = Popup(title='Ajouter un arrêt', content=layout, size_hint=(0.9, 0.5))
        
        def valider(instance):
            self.ajouter_arret_manuel(nom_input.text, heure_input.text)
            popup.dismiss()

        btn_valider.bind(on_release=valider)
        layout.add_widget(nom_input)
        layout.add_widget(heure_input)
        layout.add_widget(btn_valider)
        popup.open()