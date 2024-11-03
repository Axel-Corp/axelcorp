import cv2
import qrcode
import os
from tkinter import *
from tkinter import messagebox

# Fonction pour ajouter un article
def add_item():
    item_name = entry_name.get()
    category = entry_category.get()
    quantity = entry_quantity.get()
    location = entry_location.get()
    supplier = entry_supplier.get()

    if item_name and category and quantity and location and supplier:
        # Créer le QR code
        qr = qrcode.make(item_name)
        img_path = f"{item_name}.png"
        qr.save(img_path)

        # Ajouter l'article à la liste
        items_list.append({
            'name': item_name,
            'category': category,
            'quantity': quantity,
            'location': location,
            'supplier': supplier,
            'img_path': img_path
        })

        update_display()
        entry_name.delete(0, END)
        entry_category.delete(0, END)
        entry_quantity.delete(0, END)
        entry_location.delete(0, END)
        entry_supplier.delete(0, END)
    else:
        messagebox.showerror("Erreur", "Tous les champs doivent être remplis.")

# Fonction pour mettre à jour l'affichage des articles
def update_display():
    for widget in items_frame.winfo_children():
        widget.destroy()

    for idx, item in enumerate(items_list):
        Label(items_frame, text=item['name'], bg='#e6e6e6').grid(row=idx, column=0, sticky=W, padx=5, pady=2)
        Button(items_frame, text="Supprimer", command=lambda i=idx: remove_item(i), bg='#f44336', fg='white').grid(row=idx, column=1, padx=5, pady=2)

# Fonction pour supprimer un article
def remove_item(idx):
    os.remove(items_list[idx]['img_path'])  # Supprimer l'image du QR code
    del items_list[idx]
    update_display()

# Fonction pour scanner un QR code
def scan_qr_code():
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Essayer d'utiliser DirectShow
    detector = cv2.QRCodeDetector()

    while True:
        ret, frame = cap.read()
        if not ret:
            messagebox.showerror("Erreur", "Impossible de capturer l'image de la caméra.")
            break
        
        # Détection du QR code
        data, bbox, _ = detector(frame)

        # Si un QR code est détecté
        if bbox is not None and data:
            messagebox.showinfo("QR Code Scanné", f"Données: {data}")
            break
        
        # Afficher la vidéo
        cv2.imshow("Scan QR Code", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Fonction pour imprimer le QR code
def print_qr_code():
    item_name = entry_name.get()  # Utiliser le nom entré dans le champ
    img_path = f"{item_name}.png"
    if os.path.exists(img_path):
        try:
            os.startfile(img_path)  # Ouvrir le fichier image avec l'application par défaut
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'impression : {str(e)}")
    else:
        messagebox.showerror("Erreur", "Le QR code n'existe pas.")

# Initialisation de l'interface Tkinter
root = Tk()
root.title("Gestion d'Inventaire avec QR Codes")
root.geometry("600x400")
items_list = []

# Création des champs d'entrée
Label(root, text="Nom de l'Article", bg='#e6e6e6').grid(row=0, column=0, sticky=W, padx=5, pady=2)
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
Button(root, text="Ajouter Article", command=add_item, bg='#4CAF50', fg='white').grid(row=5, column=0, padx=5, pady=10)
Button(root, text="Imprimer QR Code", command=print_qr_code, bg='#2196F3', fg='white').grid(row=5, column=1, padx=5, pady=10)
Button(root, text="Scanner QR Code", command=scan_qr_code, bg='#FFC107', fg='white').grid(row=5, column=2, padx=5, pady=10)

# Cadre pour afficher les articles
items_frame = Frame(root, bg='#e6e6e6')
items_frame.grid(row=6, column=0, columnspan=3, pady=10, sticky='nsew')

# Exécution de l'interface
update_display()
root.mainloop()
