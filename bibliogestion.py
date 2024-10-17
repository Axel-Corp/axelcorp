import sqlite3
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime, timedelta

# Connexion à la base de données SQLite
conn = sqlite3.connect('bibliotheque.db')
c = conn.cursor()

# Création des tables (si elles n'existent pas)
c.execute('''CREATE TABLE IF NOT EXISTS livres (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titre TEXT,
                auteur TEXT)''')

c.execute('''CREATE TABLE IF NOT EXISTS emprunteurs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT,
                email TEXT)''')

c.execute('''CREATE TABLE IF NOT EXISTS emprunts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                livre_id INTEGER,
                emprunteur_id INTEGER,
                date_emprunt DATE,
                date_retour DATE,
                date_limite DATE,
                statut TEXT)''')

conn.commit()

# Initialisation de la fenêtre principale
root = Tk()
root.title("Gestion de Bibliothèque")
root.geometry("900x600")
root.minsize(800, 400)

# Fonction pour vérifier les identifiants de l'administrateur
def verifier_identifiants():
    nom_utilisateur = entry_nom_utilisateur.get()
    mot_de_passe = entry_mot_de_passe.get()

    if nom_utilisateur == "admin" and mot_de_passe == "motdepasse":
        messagebox.showinfo("Succès", "Connexion réussie !")
        fenetre_connexion.destroy()  # Fermer la fenêtre de connexion
        afficher_interface()  # Afficher l'interface principale
    else:
        messagebox.showerror("Erreur", "Nom d'utilisateur ou mot de passe incorrect")

# Fonction pour afficher la fenêtre de connexion
def afficher_connexion():
    global fenetre_connexion, entry_nom_utilisateur, entry_mot_de_passe
    fenetre_connexion = Toplevel(root)
    fenetre_connexion.title("Connexion Admin")
    
    style = ttk.Style()
    style.configure('TLabel', font=('Arial', 12))
    style.configure('TButton', font=('Arial', 12))

    label_nom_utilisateur = ttk.Label(fenetre_connexion, text="Nom d'utilisateur:")
    label_nom_utilisateur.pack(pady=5)
    entry_nom_utilisateur = ttk.Entry(fenetre_connexion)
    entry_nom_utilisateur.pack(pady=5)

    label_mot_de_passe = ttk.Label(fenetre_connexion, text="Mot de passe:")
    label_mot_de_passe.pack(pady=5)
    entry_mot_de_passe = ttk.Entry(fenetre_connexion, show="*")
    entry_mot_de_passe.pack(pady=5)

    bouton_connexion = ttk.Button(fenetre_connexion, text="Connexion", command=verifier_identifiants)
    bouton_connexion.pack(pady=10)

# Fonction pour afficher l'interface principale
def afficher_interface():
    global emprunteur_text, livre_text, historique_text, entry_titre, entry_auteur, entry_nom_emprunteur, entry_email_emprunteur, entry_livre, entry_emprunteur, entry_emprunt_a_retourner
    
    # Créer une grille ajustable pour la mise en page
    main_frame = ttk.Frame(root)
    main_frame.pack(fill=BOTH, expand=True)

    # Configuration de la grille
    main_frame.grid_columnconfigure(0, weight=1)
    main_frame.grid_columnconfigure(1, weight=1)
    main_frame.grid_columnconfigure(2, weight=1)

    # Zone pour afficher la liste des livres
    livre_text = Text(main_frame, wrap=WORD, height=10)
    livre_text.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
    afficher_livres()

    # Zone pour afficher la liste des emprunteurs
    emprunteur_text = Text(main_frame, wrap=WORD, height=10)
    emprunteur_text.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
    afficher_emprunteurs()

    # Zone pour afficher l'historique des emprunts
    historique_text = Text(main_frame, wrap=WORD, height=10)
    historique_text.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
    afficher_historique()

    # Section pour ajouter un nouveau livre
    section_livre = ttk.LabelFrame(main_frame, text="Ajouter un livre")
    section_livre.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

    ttk.Label(section_livre, text="Titre:").grid(row=0, column=0, padx=10, pady=5)
    entry_titre = ttk.Entry(section_livre)
    entry_titre.grid(row=1, column=0, padx=10, pady=5)

    ttk.Label(section_livre, text="Auteur:").grid(row=2, column=0, padx=10, pady=5)
    entry_auteur = ttk.Entry(section_livre)
    entry_auteur.grid(row=3, column=0, padx=10, pady=5)

    bouton_ajouter_livre = ttk.Button(section_livre, text="Ajouter Livre", command=ajouter_livre)
    bouton_ajouter_livre.grid(row=4, column=0, padx=10, pady=10)

    # Section pour ajouter un emprunteur
    section_emprunteur = ttk.LabelFrame(main_frame, text="Ajouter un emprunteur")
    section_emprunteur.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

    ttk.Label(section_emprunteur, text="Nom:").grid(row=0, column=0, padx=10, pady=5)
    entry_nom_emprunteur = ttk.Entry(section_emprunteur)
    entry_nom_emprunteur.grid(row=1, column=0, padx=10, pady=5)

    ttk.Label(section_emprunteur, text="Email:").grid(row=2, column=0, padx=10, pady=5)
    entry_email_emprunteur = ttk.Entry(section_emprunteur)
    entry_email_emprunteur.grid(row=3, column=0, padx=10, pady=5)

    bouton_ajouter_emprunteur = ttk.Button(section_emprunteur, text="Ajouter Emprunteur", command=ajouter_emprunteur)
    bouton_ajouter_emprunteur.grid(row=4, column=0, padx=10, pady=10)

    # Section pour ajouter un emprunt
    section_emprunt = ttk.LabelFrame(main_frame, text="Ajouter un emprunt")
    section_emprunt.grid(row=1, column=2, padx=10, pady=10, sticky="ew")

    ttk.Label(section_emprunt, text="ID Livre:").grid(row=0, column=0, padx=10, pady=5)
    entry_livre = ttk.Entry(section_emprunt)
    entry_livre.grid(row=1, column=0, padx=10, pady=5)

    ttk.Label(section_emprunt, text="ID Emprunteur:").grid(row=2, column=0, padx=10, pady=5)
    entry_emprunteur = ttk.Entry(section_emprunt)
    entry_emprunteur.grid(row=3, column=0, padx=10, pady=5)

    bouton_ajouter_emprunt = ttk.Button(section_emprunt, text="Ajouter Emprunt", command=ajouter_emprunt)
    bouton_ajouter_emprunt.grid(row=4, column=0, padx=10, pady=10)

    # Section pour retourner un emprunt
    section_retour = ttk.LabelFrame(main_frame, text="Retourner un emprunt")
    section_retour.grid(row=2, column=2, padx=10, pady=10, sticky="ew")

    ttk.Label(section_retour, text="ID Emprunt:").grid(row=0, column=0, padx=10, pady=5)
    entry_emprunt_a_retourner = ttk.Entry(section_retour)
    entry_emprunt_a_retourner.grid(row=1, column=0, padx=10, pady=5)

    bouton_retourner_emprunt = ttk.Button(section_retour, text="Retourner Emprunt", command=retourner_emprunt)
    bouton_retourner_emprunt.grid(row=2, column=0, padx=10, pady=10)

    # Ajuster le layout
    root.bind("<Configure>", ajuster_layout)

# Fonction pour retourner un emprunt
def retourner_emprunt():
    emprunt_id = entry_emprunt_a_retourner.get()

    if emprunt_id:
        c.execute("UPDATE emprunts SET date_retour = ?, statut = ? WHERE id = ?", (datetime.now(), 'Retourne', emprunt_id))
        conn.commit()
        afficher_historique()
        entry_emprunt_a_retourner.delete(0, END)
        messagebox.showinfo("Succès", "Emprunt retourné avec succès!")
    else:
        messagebox.showerror("Erreur", "Veuillez entrer l'ID de l'emprunt.")

# Fonction pour afficher les livres
def afficher_livres():
    c.execute("SELECT * FROM livres")
    livres = c.fetchall()
    livre_text.delete('1.0', END)
    if livres:
        for livre in livres:
            livre_text.insert(END, f"ID: {livre[0]}, Titre: {livre[1]}, Auteur: {livre[2]}\n")
    else:
        livre_text.insert(END, "Aucun livre disponible.\n")

# Fonction pour afficher les emprunteurs
def afficher_emprunteurs():
    c.execute("SELECT * FROM emprunteurs")
    emprunteurs = c.fetchall()
    emprunteur_text.delete('1.0', END)
    if emprunteurs:
        for emprunteur in emprunteurs:
            emprunteur_text.insert(END, f"ID: {emprunteur[0]}, Nom: {emprunteur[1]}, Email: {emprunteur[2]}\n")
    else:
        emprunteur_text.insert(END, "Aucun emprunteur enregistré.\n")

# Fonction pour afficher l'historique des emprunts
def afficher_historique():
    c.execute("SELECT * FROM emprunts")
    emprunts = c.fetchall()
    historique_text.delete('1.0', END)
    if emprunts:
        for emprunt in emprunts:
            historique_text.insert(END, f"ID Emprunt: {emprunt[0]}, ID Livre: {emprunt[1]}, ID Emprunteur: {emprunt[2]}, Date Emprunt: {emprunt[3]}, Date Retour: {emprunt[4]}\n")
    else:
        historique_text.insert(END, "Aucun emprunt enregistré.\n")

# Fonction pour ajouter un livre
def ajouter_livre():
    titre = entry_titre.get()
    auteur = entry_auteur.get()

    if titre and auteur:
        c.execute("INSERT INTO livres (titre, auteur) VALUES (?, ?)", (titre, auteur))
        conn.commit()
        afficher_livres()
        entry_titre.delete(0, END)
        entry_auteur.delete(0, END)
        messagebox.showinfo("Succès", "Livre ajouté avec succès!")
    else:
        messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")

# Fonction pour ajouter un emprunteur
def ajouter_emprunteur():
    nom = entry_nom_emprunteur.get()
    email = entry_email_emprunteur.get()

    if nom and email:
        c.execute("INSERT INTO emprunteurs (nom, email) VALUES (?, ?)", (nom, email))
        conn.commit()
        afficher_emprunteurs()
        entry_nom_emprunteur.delete(0, END)
        entry_email_emprunteur.delete(0, END)
        messagebox.showinfo("Succès", "Emprunteur ajouté avec succès!")
    else:
        messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")

# Fonction pour ajouter un emprunt
def ajouter_emprunt():
    livre_id = entry_livre.get()
    emprunteur_id = entry_emprunteur.get()
    date_emprunt = datetime.now()
    date_limite = date_emprunt + timedelta(days=30)

    if livre_id and emprunteur_id:
        c.execute("INSERT INTO emprunts (livre_id, emprunteur_id, date_emprunt, date_limite, statut) VALUES (?, ?, ?, ?, ?)",
                  (livre_id, emprunteur_id, date_emprunt, date_limite, 'Emprunté'))
        conn.commit()
        afficher_historique()
        entry_livre.delete(0, END)
        entry_emprunteur.delete(0, END)
        messagebox.showinfo("Succès", "Emprunt ajouté avec succès!")
    else:
        messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")

# Appel de la fonction pour afficher la fenêtre de connexion
afficher_connexion()

# Lancer l'interface Tkinter
root.mainloop()

# Fermer la connexion à la base de données lorsque l'application est fermée
conn.close()
