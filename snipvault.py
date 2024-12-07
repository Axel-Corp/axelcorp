import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox, Text

# Initialisation de la base de données
def init_db():
    conn = sqlite3.connect("snippets.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS snippets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            language TEXT NOT NULL,
            description TEXT,
            code TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Ajouter un snippet à la base
def add_snippet():
    title = title_entry.get().strip()
    language = lang_choice.get()
    description = desc_entry.get("1.0", tk.END).strip()
    code = code_entry.get("1.0", tk.END).strip()

    if not title or not code:
        messagebox.showerror("Erreur", "Le titre et le code sont obligatoires.")
        return

    conn = sqlite3.connect("snippets.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO snippets (title, language, description, code) VALUES (?, ?, ?, ?)",
                   (title, language, description, code))
    conn.commit()
    conn.close()

    title_entry.delete(0, tk.END)
    lang_choice.set(languages[0])  # Réinitialise le choix du langage
    desc_entry.delete("1.0", tk.END)
    code_entry.delete("1.0", tk.END)
    refresh_snippets()
    messagebox.showinfo("Succès", "Snippet ajouté avec succès.")

# Rafraîchir la liste des snippets
def refresh_snippets():
    for item in tree.get_children():
        tree.delete(item)

    conn = sqlite3.connect("snippets.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, language FROM snippets")
    for row in cursor.fetchall():
        tree.insert("", tk.END, values=row)
    conn.close()

# Afficher les détails d'un snippet
def show_snippet(event):
    selected_item = tree.selection()
    if not selected_item:
        return

    snippet_id = tree.item(selected_item[0])["values"][0]

    conn = sqlite3.connect("snippets.db")
    cursor = conn.cursor()
    cursor.execute("SELECT title, language, description, code FROM snippets WHERE id = ?", (snippet_id,))
    result = cursor.fetchone()
    conn.close()

    title_entry.delete(0, tk.END)
    title_entry.insert(0, result[0])

    # Vérifier si le langage est dans les options du combobox
    if result[1] in lang_choice['values']:
        lang_choice.set(result[1])
    else:
        print(f"Le langage {result[1]} n'est pas dans les options du combobox.")
        lang_choice.set(languages[0])  # Par défaut, on choisit le premier langage de la liste

    desc_entry.delete("1.0", tk.END)
    desc_entry.insert("1.0", result[2])

    code_entry.delete("1.0", tk.END)
    code_entry.insert("1.0", result[3])

# Supprimer un snippet
def delete_snippet():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Attention", "Veuillez sélectionner un snippet à supprimer.")
        return

    snippet_id = tree.item(selected_item[0])["values"][0]

    conn = sqlite3.connect("snippets.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM snippets WHERE id = ?", (snippet_id,))
    conn.commit()
    conn.close()

    refresh_snippets()
    messagebox.showinfo("Succès", "Snippet supprimé avec succès.")

# Interface utilisateur
root = tk.Tk()
root.title("SnipVault")

# Styles
style = ttk.Style()
style.configure("Treeview.Heading", font=("Arial", 12, "bold"))
style.configure("Treeview", font=("Arial", 10))

# Entrée pour le titre
tk.Label(root, text="Titre :", font=("Arial", 12)).grid(row=0, column=0, sticky="w")
title_entry = tk.Entry(root, width=40, font=("Arial", 12))
title_entry.grid(row=0, column=1, padx=10, pady=5)

# Liste déroulante pour le langage
languages = ["Python", "JavaScript", "HTML", "CSS", "Java", "C++"]
tk.Label(root, text="Langage :", font=("Arial", 12)).grid(row=1, column=0, sticky="w")
lang_choice = ttk.Combobox(root, values=languages, state="readonly", font=("Arial", 12))
lang_choice.grid(row=1, column=1, padx=10, pady=5)
lang_choice.set(languages[0])

# Zone de texte pour la description
tk.Label(root, text="Description :", font=("Arial", 12)).grid(row=2, column=0, sticky="nw")
desc_entry = Text(root, height=4, width=40, font=("Arial", 10))
desc_entry.grid(row=2, column=1, padx=10, pady=5)

# Zone de texte pour le code
tk.Label(root, text="Code :", font=("Arial", 12)).grid(row=3, column=0, sticky="nw")
code_entry = Text(root, height=10, width=40, font=("Courier New", 10), bg="#f4f4f4")
code_entry.grid(row=3, column=1, padx=10, pady=5)

# Boutons
add_btn = tk.Button(root, text="Ajouter", command=add_snippet, bg="#4CAF50", fg="white", font=("Arial", 12))
add_btn.grid(row=4, column=0, padx=10, pady=10)

delete_btn = tk.Button(root, text="Supprimer", command=delete_snippet, bg="#f44336", fg="white", font=("Arial", 12))
delete_btn.grid(row=4, column=1, padx=10, pady=10, sticky="e")

# Liste des snippets
tree = ttk.Treeview(root, columns=("ID", "Titre", "Langage"), show="headings", height=10)
tree.heading("ID", text="ID")
tree.heading("Titre", text="Titre")
tree.heading("Langage", text="Langage")
tree.column("ID", width=50)
tree.column("Titre", width=200)
tree.column("Langage", width=100)
tree.grid(row=5, column=0, columnspan=2, padx=10, pady=10)
tree.bind("<Double-1>", show_snippet)

# Initialisation
init_db()
refresh_snippets()

root.mainloop()
