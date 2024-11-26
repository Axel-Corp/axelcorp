import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk
from tkinter import font

# Connexion à la base de données
def get_db_connection():
    return sqlite3.connect('clientlink.db')

# Créer la base de données et les tables
def create_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS clients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT,
        prenom TEXT,
        email TEXT,
        telephone TEXT,
        adresse TEXT
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS opportunites (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_id INTEGER,
        produit TEXT,
        montant REAL,
        date_cloture TEXT,
        statut TEXT,
        FOREIGN KEY (client_id) REFERENCES clients (id)
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS taches (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_id INTEGER,
        description TEXT,
        date_limite TEXT,
        statut TEXT,
        FOREIGN KEY (client_id) REFERENCES clients (id)
    )''')

    conn.commit()
    conn.close()

# Ajouter un client
def ajouter_client():
    nom = entry_nom.get()
    prenom = entry_prenom.get()
    email = entry_email.get()
    telephone = entry_telephone.get()
    adresse = entry_adresse.get()

    if nom and prenom and email:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO clients (nom, prenom, email, telephone, adresse) VALUES (?, ?, ?, ?, ?)",
                       (nom, prenom, email, telephone, adresse))
        conn.commit()
        conn.close()
        messagebox.showinfo("Succès", "Client ajouté avec succès !")
        refresh_clients()
    else:
        messagebox.showwarning("Erreur", "Veuillez remplir tous les champs obligatoires.")

# Ajouter une opportunité
def ajouter_opportunite():
    client_id = entry_client_id.get()
    produit = entry_produit.get()
    montant = entry_montant.get()
    date_cloture = entry_date_cloture.get()
    statut = entry_statut.get()

    if client_id and produit and montant and statut:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO opportunites (client_id, produit, montant, date_cloture, statut) VALUES (?, ?, ?, ?, ?)",
                       (client_id, produit, montant, date_cloture, statut))
        conn.commit()
        conn.close()
        messagebox.showinfo("Succès", "Opportunité ajoutée avec succès !")
        refresh_opportunites()
    else:
        messagebox.showwarning("Erreur", "Veuillez remplir tous les champs obligatoires.")

# Ajouter une tâche
def ajouter_tache():
    client_id = entry_client_id_tache.get()
    description = entry_description.get()
    date_limite = entry_date_limite.get()
    statut = entry_statut_tache.get()

    if client_id and description and date_limite and statut:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO taches (client_id, description, date_limite, statut) VALUES (?, ?, ?, ?)",
                       (client_id, description, date_limite, statut))
        conn.commit()
        conn.close()
        messagebox.showinfo("Succès", "Tâche ajoutée avec succès !")
        refresh_taches()
    else:
        messagebox.showwarning("Erreur", "Veuillez remplir tous les champs obligatoires.")

# Rafraîchir la liste des clients
def refresh_clients():
    for row in tree_clients.get_children():
        tree_clients.delete(row)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clients")
    clients = cursor.fetchall()
    for client in clients:
        tree_clients.insert('', 'end', values=client[1:])
    conn.close()

# Rafraîchir la liste des opportunités
def refresh_opportunites():
    for row in tree_opportunites.get_children():
        tree_opportunites.delete(row)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM opportunites")
    opportunites = cursor.fetchall()
    for opp in opportunites:
        tree_opportunites.insert('', 'end', values=opp[1:])
    conn.close()

# Rafraîchir la liste des tâches
def refresh_taches():
    for row in tree_taches.get_children():
        tree_taches.delete(row)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM taches")
    taches = cursor.fetchall()
    for tache in taches:
        tree_taches.insert('', 'end', values=tache[1:])
    conn.close()

# Fenêtre principale
root = tk.Tk()
root.title("ClientLink - CRM Complet")
root.geometry("950x600")
root.config(bg="#f5f5f5")

# Polices personnalisées
title_font = font.Font(family="Helvetica", size=16, weight="bold")
label_font = font.Font(family="Arial", size=10)
button_font = font.Font(family="Arial", size=10, weight="bold")

# Créer la base de données si elle n'existe pas
create_db()

# Interface client
frame_client = tk.LabelFrame(root, text="Ajouter un client", padx=10, pady=10, bg="#ffffff", bd=2, relief="solid")
frame_client.grid(row=0, column=0, padx=20, pady=20)

tk.Label(frame_client, text="Nom", font=label_font, bg="#ffffff").grid(row=0, column=0, pady=5)
entry_nom = tk.Entry(frame_client, font=label_font)
entry_nom.grid(row=0, column=1, pady=5)

tk.Label(frame_client, text="Prénom", font=label_font, bg="#ffffff").grid(row=1, column=0, pady=5)
entry_prenom = tk.Entry(frame_client, font=label_font)
entry_prenom.grid(row=1, column=1, pady=5)

tk.Label(frame_client, text="Email", font=label_font, bg="#ffffff").grid(row=2, column=0, pady=5)
entry_email = tk.Entry(frame_client, font=label_font)
entry_email.grid(row=2, column=1, pady=5)

tk.Label(frame_client, text="Téléphone", font=label_font, bg="#ffffff").grid(row=3, column=0, pady=5)
entry_telephone = tk.Entry(frame_client, font=label_font)
entry_telephone.grid(row=3, column=1, pady=5)

tk.Label(frame_client, text="Adresse", font=label_font, bg="#ffffff").grid(row=4, column=0, pady=5)
entry_adresse = tk.Entry(frame_client, font=label_font)
entry_adresse.grid(row=4, column=1, pady=5)

tk.Button(frame_client, text="Ajouter Client", font=button_font, bg="#4CAF50", fg="white", command=ajouter_client).grid(row=5, column=0, columnspan=2, pady=10)

# Interface opportunité
frame_opportunite = tk.LabelFrame(root, text="Ajouter une opportunité", padx=10, pady=10, bg="#ffffff", bd=2, relief="solid")
frame_opportunite.grid(row=1, column=0, padx=20, pady=20)

tk.Label(frame_opportunite, text="ID Client", font=label_font, bg="#ffffff").grid(row=0, column=0, pady=5)
entry_client_id = tk.Entry(frame_opportunite, font=label_font)
entry_client_id.grid(row=0, column=1, pady=5)

tk.Label(frame_opportunite, text="Produit", font=label_font, bg="#ffffff").grid(row=1, column=0, pady=5)
entry_produit = tk.Entry(frame_opportunite, font=label_font)
entry_produit.grid(row=1, column=1, pady=5)

tk.Label(frame_opportunite, text="Montant", font=label_font, bg="#ffffff").grid(row=2, column=0, pady=5)
entry_montant = tk.Entry(frame_opportunite, font=label_font)
entry_montant.grid(row=2, column=1, pady=5)

tk.Label(frame_opportunite, text="Date Clôture", font=label_font, bg="#ffffff").grid(row=3, column=0, pady=5)
entry_date_cloture = tk.Entry(frame_opportunite, font=label_font)
entry_date_cloture.grid(row=3, column=1, pady=5)

tk.Label(frame_opportunite, text="Statut", font=label_font, bg="#ffffff").grid(row=4, column=0, pady=5)
entry_statut = tk.Entry(frame_opportunite, font=label_font)
entry_statut.grid(row=4, column=1, pady=5)

tk.Button(frame_opportunite, text="Ajouter Opportunité", font=button_font, bg="#4CAF50", fg="white", command=ajouter_opportunite).grid(row=5, column=0, columnspan=2, pady=10)

# Interface tâche
frame_tache = tk.LabelFrame(root, text="Ajouter une tâche", padx=10, pady=10, bg="#ffffff", bd=2, relief="solid")
frame_tache.grid(row=2, column=0, padx=20, pady=20)

tk.Label(frame_tache, text="ID Client", font=label_font, bg="#ffffff").grid(row=0, column=0, pady=5)
entry_client_id_tache = tk.Entry(frame_tache, font=label_font)
entry_client_id_tache.grid(row=0, column=1, pady=5)

tk.Label(frame_tache, text="Description", font=label_font, bg="#ffffff").grid(row=1, column=0, pady=5)
entry_description = tk.Entry(frame_tache, font=label_font)
entry_description.grid(row=1, column=1, pady=5)

tk.Label(frame_tache, text="Date Limite", font=label_font, bg="#ffffff").grid(row=2, column=0, pady=5)
entry_date_limite = tk.Entry(frame_tache, font=label_font)
entry_date_limite.grid(row=2, column=1, pady=5)

tk.Label(frame_tache, text="Statut", font=label_font, bg="#ffffff").grid(row=3, column=0, pady=5)
entry_statut_tache = tk.Entry(frame_tache, font=label_font)
entry_statut_tache.grid(row=3, column=1, pady=5)

tk.Button(frame_tache, text="Ajouter Tâche", font=button_font, bg="#4CAF50", fg="white", command=ajouter_tache).grid(row=4, column=0, columnspan=2, pady=10)

# Interface TreeViews
frame_tables = tk.Frame(root, bg="#ffffff")
frame_tables.grid(row=0, column=1, rowspan=3, padx=20, pady=20)

# Tableau des clients
tree_clients = ttk.Treeview(frame_tables, columns=("Nom", "Prénom", "Email", "Téléphone", "Adresse"), show="headings")
tree_clients.heading("Nom", text="Nom")
tree_clients.heading("Prénom", text="Prénom")
tree_clients.heading("Email", text="Email")
tree_clients.heading("Téléphone", text="Téléphone")
tree_clients.heading("Adresse", text="Adresse")
tree_clients.grid(row=0, column=0, pady=10)

# Tableau des opportunités
tree_opportunites = ttk.Treeview(frame_tables, columns=("Client", "Produit", "Montant", "Date Clôture", "Statut"), show="headings")
tree_opportunites.heading("Client", text="Client")
tree_opportunites.heading("Produit", text="Produit")
tree_opportunites.heading("Montant", text="Montant")
tree_opportunites.heading("Date Clôture", text="Date Clôture")
tree_opportunites.heading("Statut", text="Statut")
tree_opportunites.grid(row=1, column=0, pady=10)

# Tableau des tâches
tree_taches = ttk.Treeview(frame_tables, columns=("Client", "Description", "Date Limite", "Statut"), show="headings")
tree_taches.heading("Client", text="Client")
tree_taches.heading("Description", text="Description")
tree_taches.heading("Date Limite", text="Date Limite")
tree_taches.heading("Statut", text="Statut")
tree_taches.grid(row=2, column=0, pady=10)

# Rafraîchir les données au démarrage
refresh_clients()
refresh_opportunites()
refresh_taches()

root.mainloop()
