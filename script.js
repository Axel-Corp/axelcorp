// Initialiser les données dans LocalStorage si elles n'existent pas
if (!localStorage.getItem("downloads")) {
    localStorage.setItem("downloads", JSON.stringify({}));
}

// Fonction pour enregistrer un téléchargement
function trackDownload(programName) {
    // Récupérer les données actuelles
    const downloads = JSON.parse(localStorage.getItem("downloads"));

    // Incrémenter le compteur pour le programme
    downloads[programName] = (downloads[programName] || 0) + 1;

    // Sauvegarder les données mises à jour
    localStorage.setItem("downloads", JSON.stringify(downloads));

    // Mettre à jour l'affichage
    updateStats();
}

// Fonction pour mettre à jour le tableau des statistiques
function updateStats() {
    const downloads = JSON.parse(localStorage.getItem("downloads"));
    const statsBody = document.getElementById("stats-body");

    // Vider le tableau existant
    statsBody.innerHTML = "";

    // Ajouter chaque programme et ses téléchargements
    for (const [program, count] of Object.entries(downloads)) {
        const row = document.createElement("tr");
        row.innerHTML = `<td>${program}</td><td>${count}</td>`;
        statsBody.appendChild(row);
    }
}

// Mettre à jour les statistiques à l'ouverture de la page
updateStats();
