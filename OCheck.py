import tkinter as tk
from tkinter import messagebox
import psutil
import platform
import cpuinfo

class OCheckerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("OChecker - Validation d'Overclocking")
        self.root.geometry("500x650")
        
        self.data = {}
        
        # Initialisation de l'interface
        self.setup_ui()
        self.detect_hardware()

    def setup_ui(self):
        tk.Label(self.root, text="OChecker", font=("Arial", 18, "bold")).pack(pady=10)
        
        # Affichage des informations détectées
        self.info_frame = tk.Frame(self.root, padx=10, pady=10)
        self.info_frame.pack(fill="both", expand=True)

        self.info_label = tk.Label(self.info_frame, text="Informations des composants détectés :", font=("Arial", 12, "bold"))
        self.info_label.pack(anchor="w")

        self.info_text = tk.Text(self.info_frame, height=12, state="disabled", wrap="word", bg="#f0f0f0")
        self.info_text.pack(fill="both", expand=True)

        # Entrées utilisateur
        tk.Label(self.root, text="Paramètres d'Overclocking", font=("Arial", 12, "bold")).pack(pady=10)
        
        tk.Label(self.root, text="Support Overclocking (oui/non) :").pack(anchor="w", padx=10)
        self.overclock_supported = tk.Entry(self.root)
        self.overclock_supported.pack(fill="x", padx=10)
        
        tk.Label(self.root, text="Système de refroidissement (air/eau) :").pack(anchor="w", padx=10)
        self.cooling_system = tk.Entry(self.root)
        self.cooling_system.pack(fill="x", padx=10)
        
        # Zone pour afficher l'overclocking recommandé
        self.recommended_label = tk.Label(self.root, text="Overclocking recommandé :", font=("Arial", 12, "bold"))
        self.recommended_label.pack(pady=10)

        self.recommended_overclocking = tk.Label(self.root, text="", font=("Arial", 10))
        self.recommended_overclocking.pack(pady=10)

        # Zone pour entrer manuellement la fréquence d'overclocking
        tk.Label(self.root, text="Entrez votre fréquence d'overclocking manuelle (GHz) :").pack(anchor="w", padx=10)
        self.manual_overclock = tk.Entry(self.root)
        self.manual_overclock.pack(fill="x", padx=10)

        # Bouton de validation
        self.validate_button = tk.Button(self.root, text="Valider Overclocking", command=self.validate_overclocking)
        self.validate_button.pack(pady=20)
    
    def detect_hardware(self):
        # Détection des composants matériels
        self.data['cpu_name'] = cpuinfo.get_cpu_info().get('brand_raw', 'Inconnu')
        self.data['base_freq'] = float(cpuinfo.get_cpu_info().get('hz_advertised_friendly', '0.0 GHz').split()[0])
        self.data['max_freq_cpu'] = float(cpuinfo.get_cpu_info().get('hz_actual_friendly', '0.0 GHz').split()[0])
        self.data['ram_size'] = round(psutil.virtual_memory().total / (1024 ** 3))  # RAM en Go
        self.data['os'] = platform.system() + " " + platform.version()

        # Affichage dans l'interface
        self.info_text.config(state="normal")
        self.info_text.delete("1.0", tk.END)
        self.info_text.insert(tk.END, f"Processeur : {self.data['cpu_name']}\n")
        self.info_text.insert(tk.END, f"Fréquence de base : {self.data['base_freq']} GHz\n")
        self.info_text.insert(tk.END, f"Fréquence maximale supportée : {self.data['max_freq_cpu']} GHz\n")
        self.info_text.insert(tk.END, f"RAM : {self.data['ram_size']} Go\n")
        self.info_text.insert(tk.END, f"Système d'exploitation : {self.data['os']}\n")
        self.info_text.config(state="disabled")

        # Calculer l'overclocking recommandé
        self.calculate_recommended_overclocking()

    def calculate_recommended_overclocking(self):
        # Logic pour calculer l'overclocking recommandé en fonction de la fréquence de base
        overclock_factor = 1.1  # Facteur d'overclocking pour une augmentation de 10%
        
        if "k" in self.data['cpu_name'].lower() or "kf" in self.data['cpu_name'].lower():
            recommended_frequency = self.data['base_freq'] * overclock_factor
            cooling_message = "Refroidissement par air ou par eau recommandé"
        else:
            recommended_frequency = self.data['base_freq']
            cooling_message = "Overclocking non recommandé pour ce processeur."

        # Afficher la fréquence recommandée
        self.recommended_overclocking.config(text=f"Fréquence recommandée : {recommended_frequency:.2f} GHz\n{cooling_message}")

    def validate_overclocking(self):
        # Récupération des valeurs saisies
        overclock_supported = self.overclock_supported.get().strip().lower()
        cooling_system = self.cooling_system.get().strip().lower()
        manual_overclock = self.manual_overclock.get().strip()

        # Vérification du support de l'overclocking
        if "k" not in self.data['cpu_name'].lower() and "kf" not in self.data['cpu_name'].lower():
            messagebox.showwarning("Validation échouée", "Le processeur ne supporte pas l'overclocking.")
            return

        if overclock_supported != "oui":
            messagebox.showwarning("Validation échouée", "L'overclocking n'est pas activé dans les paramètres.")
            return

        if manual_overclock:
            try:
                user_overclock = float(manual_overclock)
            except ValueError:
                messagebox.showwarning("Validation échouée", "Veuillez entrer une valeur numérique pour l'overclocking.")
                return

            if user_overclock > self.data['max_freq_cpu']:
                messagebox.showwarning("Validation échouée", "La fréquence d'overclocking dépasse la limite maximale du processeur.")
                return

            if cooling_system == "air" and user_overclock > self.data['base_freq'] * 1.3:
                messagebox.showwarning("Validation échouée", "Le refroidissement par air peut ne pas être suffisant pour ce niveau d'overclocking.")
                return

            if cooling_system == "eau" and user_overclock > self.data['base_freq'] * 1.5:
                messagebox.showwarning("Validation échouée", "Même avec un refroidissement par eau, ce niveau d'overclocking peut être risqué.")
                return

            # Succès
            messagebox.showinfo("Validation réussie", f"L'overclocking manuel est validé avec {user_overclock} GHz.")
        else:
            # Si l'utilisateur ne saisit pas d'overclocking manuel, utiliser la fréquence recommandée
            recommended_frequency = self.data['base_freq'] * 1.1
            messagebox.showinfo("Validation réussie", f"L'overclocking recommandé est validé à {recommended_frequency:.2f} GHz.")

# Exécution de l'application
if __name__ == "__main__":
    root = tk.Tk()
    app = OCheckerApp(root)
    root.mainloop()
