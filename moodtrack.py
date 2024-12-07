import tkinter as tk
from tkinter import messagebox
import json
from datetime import datetime

# Fonction pour sauvegarder les données de l'humeur dans un fichier JSON
def save_mood(mood, note):
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Charger les données existantes depuis le fichier
    try:
        with open("moods.json", "r") as file:
            all_moods = json.load(file)
    except FileNotFoundError:
        all_moods = []
    
    # Vérifier si une humeur a déjà été enregistrée pour aujourd'hui
    for mood_data in all_moods:
        if mood_data['date'].startswith(today):
            messagebox.showerror("Erreur", "Vous avez déjà enregistré votre humeur pour aujourd'hui.")
            return
    
    # Si aucune humeur n'a été enregistrée pour aujourd'hui, on l'ajoute
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    mood_data = {
        "date": date,
        "mood": mood,
        "note": note
    }
    
    # Ajouter la nouvelle humeur et la sauvegarder dans le fichier
    all_moods.append(mood_data)
    with open("moods.json", "w") as file:
        json.dump(all_moods, file, indent=4)
    
    messagebox.showinfo("Succès", "Votre humeur a été enregistrée.")
    
    # Mettre à jour l'affichage de l'historique
    update_history()

# Fonction pour afficher l'historique des humeurs
def update_history():
    try:
        with open("moods.json", "r") as file:
            all_moods = json.load(file)
    except FileNotFoundError:
        all_moods = []

    # Vider la zone d'affichage de l'historique
    for widget in history_frame.winfo_children():
        widget.destroy()

    # Afficher chaque entrée de l'historique
    for mood_data in all_moods:
        mood_label = f"{mood_data['date']} - Humeur: {mood_data['mood']} - Note: {mood_data['note']}"
        label = tk.Label(history_frame, text=mood_label, anchor="w")
        label.pack(fill='x')

# Fonction pour fournir des conseils en fonction de l'humeur
def give_advice(mood):
    advice = {
        "joyeux": "Continuez à profiter de votre bonne humeur ! Pensez à pratiquer la gratitude.",
        "triste": "Prenez du temps pour vous et faites une activité que vous aimez, même si ce n'est que pour quelques minutes.",
        "stressé": "Essayez une technique de respiration profonde ou de méditation pour réduire le stress.",
        "calme": "Prenez ce moment pour réfléchir positivement et profiter de la tranquillité.",
        "en colère": "Pratiquez des exercices de respiration ou faites une petite promenade pour calmer vos nerfs."
    }
    
    return advice.get(mood, "Rappelez-vous de prendre soin de vous, peu importe l'humeur!")

# Fonction principale pour l'interface
def submit_mood():
    mood = mood_var.get()
    note = note_entry.get()
    
    if mood == "":
        messagebox.showerror("Erreur", "Veuillez sélectionner une humeur.")
        return
    
    save_mood(mood, note)
    
    # Afficher des conseils en fonction de l'humeur choisie
    advice = give_advice(mood)
    advice_label.config(text=advice)

# Création de la fenêtre principale
window = tk.Tk()
window.title("MoodTracker")

# Sélection de l'humeur
mood_var = tk.StringVar(value="")
moods = ["joyeux", "triste", "stressé", "calme", "en colère"]
mood_label = tk.Label(window, text="Sélectionnez votre humeur :")
mood_label.pack()

for mood in moods:
    tk.Radiobutton(window, text=mood.capitalize(), variable=mood_var, value=mood).pack()

# Zone de saisie de la note
note_label = tk.Label(window, text="Ajouter une note (facultatif) :")
note_label.pack()

note_entry = tk.Entry(window, width=50)
note_entry.pack()

# Bouton pour soumettre l'humeur
submit_button = tk.Button(window, text="Soumettre", command=submit_mood)
submit_button.pack()

# Section pour afficher l'historique
history_label = tk.Label(window, text="Historique des humeurs :")
history_label.pack()

# Frame pour afficher l'historique des humeurs
history_frame = tk.Frame(window)
history_frame.pack(fill='both', expand=True)

# Label pour afficher les conseils
advice_label = tk.Label(window, text="", wraplength=300)
advice_label.pack()

# Mettre à jour l'affichage de l'historique dès l'ouverture
update_history()

# Lancer l'application
window.mainloop()
