import sqlite3
from tkinter import *
from tkinter import messagebox, ttk

# Connexion à la base de données
conn = sqlite3.connect('inventipro.db')
c = conn.cursor()

# Création des tables nécessaires
c.execute('''CREATE TABLE IF NOT EXISTS inventory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_name TEXT NOT NULL,
                category TEXT,
                quantity INTEGER NOT NULL,
                location TEXT,
                supplier TEXT,
                needs_restock BOOLEAN DEFAULT 0
            )''')
conn.commit()

# Fonction d'ajout d'un article
def add_item():
    item_name = entry_name.get()
    category = entry_category.get()
    quantity = int(entry_quantity.get())
    location = entry_location.get()
    supplier = entry_supplier.get()
    needs_restock = 1 if quantity < 10 else 0  # Réapprovisionnement si la quantité est basse

    c.execute("INSERT INTO inventory (item_name, category, quantity, location, supplier, needs_restock) VALUES (?, ?, ?, ?, ?, ?)",
              (item_name, category, quantity, location, supplier, needs_restock))
    conn.commit()
    update_display()
    clear_entries()
    messagebox.showinfo("Succès", f"{item_name} ajouté avec succès dans l'inventaire.")

# Fonction pour mettre à jour l'affichage de l'inventaire
def update_display():
    for widget in items_frame.winfo_children():
        widget.destroy()
        
    c.execute("SELECT * FROM inventory")
    items = c.fetchall()
    
    for item in items:
        item_frame = Frame(items_frame, bg='#f0f0f0', pady=5, padx=5)
        item_frame.pack(fill='x', padx=5, pady=2)

        restock_text = " - Réapprovisionnement requis" if item[6] else ""
        item_text = f"{item[1]} | Catégorie: {item[2]} | Quantité: {item[3]} | Emplacement: {item[4]}{restock_text}"
        label = Label(item_frame, text=item_text, anchor="w", font=("Arial", 10), bg='#f0f0f0')
        label.pack(side=LEFT, fill="x", expand=True)

        delete_button = Button(item_frame, text="Supprimer", command=lambda i=item[0]: delete_item(i), bg='#ff4d4d', fg='white')
        delete_button.pack(side=RIGHT)

# Fonction pour supprimer un article
def delete_item(item_id):
    c.execute("DELETE FROM inventory WHERE id = ?", (item_id,))
    conn.commit()
    update_display()
    messagebox.showinfo("Suppression", "Article supprimé avec succès de l'inventaire.")

# Fonction pour nettoyer les champs de saisie
def clear_entries():
    entry_name.delete(0, END)
    entry_category.delete(0, END)
    entry_quantity.delete(0, END)
    entry_location.delete(0, END)
    entry_supplier.delete(0, END)

# Interface graphique
root = Tk()
root.title("InventiPro - Gestion d'Inventaire d'Entreprise")
root.configure(bg='#e6e6e6')

style = ttk.Style()
style.configure("TButton", padding=6, font=("Arial", 10))

# Champs de saisie
Label(root, text="Nom de l'article", bg='#e6e6e6').grid(row=0, column=0, sticky=W, padx=5, pady=2)
entry_name = Entry(root)
entry_name.grid(row=0, column=1, pady=2)

Label(root, text="Catégorie", bg='#e6e6e6').grid(row=1, column=0, sticky=W, padx=5, pady=2)
entry_category = Entry(root)
entry_category.grid(row=1, column=1, pady=2)

Label(root, text="Quantité", bg='#e6e6e6').grid(row=2, column=0, sticky=W, padx=5, pady=2)
entry_quantity = Entry(root)
entry_quantity.grid(row=2, column=1, pady=2)

Label(root, text="Emplacement", bg='#e6e6e6').grid(row=3, column=0, sticky=W, padx=5, pady=2)
entry_location = Entry(root)
entry_location.grid(row=3, column=1, pady=2)

Label(root, text="Fournisseur", bg='#e6e6e6').grid(row=4, column=0, sticky=W, padx=5, pady=2)
entry_supplier = Entry(root)
entry_supplier.grid(row=4, column=1, pady=2)

# Boutons
Button(root, text="Ajouter", command=add_item, bg='#4CAF50', fg='white').grid(row=5, column=0, pady=10)
Button(root, text="Effacer", command=clear_entries, bg='#f39c12', fg='white').grid(row=5, column=1, pady=10)

# Cadre pour afficher les éléments de l'inventaire
items_frame = Frame(root, bg='#e6e6e6')
items_frame.grid(row=6, column=0, columnspan=2, pady=10, padx=5)

# Mise à jour initiale de l'affichage
update_display()

root.mainloop()

# Fermer la connexion à la base de données à la fin
conn.close()

