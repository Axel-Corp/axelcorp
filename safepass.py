import tkinter as tk
from tkinter import messagebox, ttk
import random
import string
import json
from cryptography.fernet import Fernet

# Génération de la clé de chiffrement (à faire une seule fois)
KEY_FILE = "secret.key"
DATA_FILE = "passwords.json"

def generate_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as key_file:
        key_file.write(key)

def load_key():
    try:
        with open(KEY_FILE, "rb") as key_file:
            return key_file.read()
    except FileNotFoundError:
        generate_key()
        return load_key()

encryption_key = load_key()
cipher = Fernet(encryption_key)

def generate_password():
    chars = string.ascii_letters + string.digits + string.punctuation
    password = "".join(random.choice(chars) for _ in range(16))
    password_entry.delete(0, tk.END)
    password_entry.insert(0, password)

def save_password():
    service = service_entry.get()
    password = password_entry.get()
    
    if not service or not password:
        messagebox.showwarning("Erreur", "Veuillez remplir tous les champs.")
        return
    
    encrypted_password = cipher.encrypt(password.encode()).decode()
    
    try:
        with open(DATA_FILE, "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}
    
    data[service] = encrypted_password
    
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)
    
    messagebox.showinfo("Succès", "Mot de passe enregistré !")

def retrieve_password():
    service = service_entry.get()
    
    try:
        with open(DATA_FILE, "r") as file:
            data = json.load(file)
        
        if service in data:
            decrypted_password = cipher.decrypt(data[service].encode()).decode()
            password_entry.delete(0, tk.END)
            password_entry.insert(0, decrypted_password)
        else:
            messagebox.showwarning("Erreur", "Aucun mot de passe trouvé pour ce service.")
    except (FileNotFoundError, json.JSONDecodeError):
        messagebox.showwarning("Erreur", "Aucune donnée trouvée.")

def delete_password():
    service = service_entry.get()
    
    try:
        with open(DATA_FILE, "r") as file:
            data = json.load(file)
        
        if service in data:
            del data[service]
            with open(DATA_FILE, "w") as file:
                json.dump(data, file, indent=4)
            messagebox.showinfo("Succès", "Mot de passe supprimé !")
        else:
            messagebox.showwarning("Erreur", "Aucun mot de passe trouvé pour ce service.")
    except (FileNotFoundError, json.JSONDecodeError):
        messagebox.showwarning("Erreur", "Aucune donnée trouvée.")

# Interface Tkinter améliorée
root = tk.Tk()
root.title("SafePass - Gestionnaire de Mots de Passe")
root.geometry("400x300")
root.resizable(False, False)
root.configure(bg="#2c3e50")

# Labels et champs
style = ttk.Style()
style.configure("TLabel", background="#2c3e50", foreground="white")
style.configure("TButton", background="#3498db", foreground="white")

service_label = ttk.Label(root, text="Service :")
service_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
service_entry = ttk.Entry(root, width=30)
service_entry.grid(row=0, column=1, padx=10, pady=10)

password_label = ttk.Label(root, text="Mot de Passe :")
password_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
password_entry = ttk.Entry(root, width=30)
password_entry.grid(row=1, column=1, padx=10, pady=10)

# Boutons améliorés
generate_button = ttk.Button(root, text="Générer", command=generate_password)
generate_button.grid(row=1, column=2, padx=10, pady=10)

save_button = ttk.Button(root, text="Enregistrer", command=save_password)
save_button.grid(row=2, column=0, columnspan=2, pady=10)

retrieve_button = ttk.Button(root, text="Récupérer", command=retrieve_password)
retrieve_button.grid(row=3, column=0, columnspan=2, pady=10)

delete_button = ttk.Button(root, text="Supprimer", command=delete_password)
delete_button.grid(row=4, column=0, columnspan=2, pady=10)

root.mainloop()