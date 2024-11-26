import os
import urllib.request
import zipfile
import subprocess
import sys
import tkinter as tk
from tkinter import messagebox

# Définir le chemin de base où les applications seront installées
base_path = os.path.expanduser("~/Documents/AxelCorp")

# Vérifier si le dossier existe, sinon le créer
if not os.path.exists(base_path):
    os.makedirs(base_path)

# Liste des applications avec leurs noms affichés, les URLs de téléchargement et types (script ou zip)
app_list = {
    "Bibliomanage": {"script": "bibliogestion.py", "url": "https://axelcorp.netlify.app/bibliogestion.py"},
    "Inventipro v1": {"script": "inventipro.py", "url": "https://axelcorp.netlify.app/inventipro.py"},
    "Inventipro v2": {"script": "inventiprov2.py", "url": "https://axelcorp.netlify.app/inventiprov2.py"},
    "Abentipro": {"script": "absentipro.zip", "url": "https://axelcorp.netlify.app/absentipro.zip", "zip": True},
    "Ocheck": {"script": "ocheck.py", "url": "https://axelcorp.netlify.app/ocheck.py"},
    "ClientLink": {"script": "clientlink.py", "url": "https://axelcorp.netlify.app/clientlink.py"}
}

# Fonction pour vérifier si une dépendance est installée
def is_dependency_installed(dependency):
    try:
        __import__(dependency)
        return True
    except ImportError:
        return False

# Fonction pour installer les dépendances nécessaires
def install_dependencies(dependencies):
    for dep in dependencies:
        if not is_dependency_installed(dep):
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", dep])
                print(f"{dep} installé avec succès.")
            except Exception as e:
                print(f"Erreur lors de l'installation de {dep}: {e}")
        else:
            print(f"{dep} est déjà installé.")

# Fonction pour télécharger et installer l'application
def install_app(app_name):
    app_info = app_list[app_name]
    app_url = app_info['url']
    app_path = os.path.join(base_path, app_info['script'])
    
    # Installer les dépendances si elles ne sont pas déjà installées
    if not os.path.exists(app_path):
        try:
            print(f"Téléchargement de {app_name} depuis {app_url}...")
            
            # Si c'est un zip, on télécharge le fichier zip et on l'extrait
            if app_info.get('zip', False):
                zip_path = os.path.join(base_path, f"{app_name}.zip")
                urllib.request.urlretrieve(app_url, zip_path)
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(base_path)
                os.remove(zip_path)  # Supprimer le fichier zip une fois extrait
                print(f"{app_name} installé avec succès à partir du fichier zip.")
            else:
                # Télécharger le fichier script Python
                urllib.request.urlretrieve(app_url, app_path)
                print(f"{app_name} installé avec succès.")
            
            # Installer les dépendances nécessaires uniquement pour cette application
            install_dependencies(["tkinter", "sqlite3"])
            
            # Mettre à jour les boutons pour afficher "Lancer" après l'installation
            update_buttons()
            
            return True
        except Exception as e:
            print(f"Erreur lors du téléchargement de {app_name}: {e}")
            messagebox.showerror("Erreur", f"Erreur lors de l'installation de {app_name}.")
            return False
    else:
        print(f"{app_name} est déjà installé.")
        return True

# Fonction pour lancer l'application
def launch_app(app_name):
    app_info = app_list[app_name]
    app_path = os.path.join(base_path, app_info['script'])
    if os.path.exists(app_path):
        subprocess.run([sys.executable, app_path])
    else:
        print(f"Erreur : {app_name} n'a pas été trouvé à l'emplacement spécifié.")
        messagebox.showerror("Erreur", f"{app_name} n'est pas installé correctement.")

# Fonction pour mettre à jour les boutons en fonction de l'installation des applications
def update_buttons():
    app_names = list(app_list.keys())
    
    for idx, app_name in enumerate(app_names):
        app_info = app_list[app_name]
        app_installed = os.path.exists(os.path.join(base_path, app_info['script']))
        
        # Mise à jour des boutons Installer / Lancer
        install_button = app_info['install_button']
        launch_button = app_info['launch_button']
        
        if app_installed:
            install_button.grid_forget()  # Cacher le bouton Installer
            launch_button.grid(row=idx+1, column=1, pady=10)  # Afficher le bouton Lancer
        else:
            install_button.grid(row=idx+1, column=0, pady=10)  # Afficher le bouton Installer
            launch_button.grid_forget()  # Cacher le bouton Lancer

# Création de la fenêtre principale
root = tk.Tk()
root.title("Axel Hub")
root.geometry("400x400")
root.config(bg="#f0f0f0")

# Ajouter des boutons pour installer et lancer les applications
for idx, (app_name, app_info) in enumerate(app_list.items()):
    # Création du bouton Installer
    install_button = tk.Button(root, text=f"Installer {app_name}", width=20, height=2,
                               command=lambda app_name=app_name: install_app(app_name))
    # Création du bouton Lancer
    launch_button = tk.Button(root, text=f"Lancer {app_name}", width=20, height=2,
                              command=lambda app_name=app_name: launch_app(app_name))

    # Ajouter les boutons à l'application
    app_info['install_button'] = install_button
    app_info['launch_button'] = launch_button

    # Initialisation de l'affichage des boutons
    install_button.grid(row=idx+1, column=0, pady=10)
    launch_button.grid_forget()  # Cacher les boutons Lancer au début

# Mettre à jour les boutons après installation
update_buttons()

# Lancer l'interface graphique
root.mainloop()
