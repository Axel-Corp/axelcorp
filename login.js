// =========================
// 1. Initialisation IndexedDB
// =========================
let db;

// Ouvre ou crée la base de données
const request = indexedDB.open("AxelCorpDB", 1);

request.onupgradeneeded = function(event) {
    db = event.target.result;

    // Crée un objet de stockage "users" s'il n'existe pas
    if (!db.objectStoreNames.contains("users")) {
        const usersStore = db.createObjectStore("users", { keyPath: "id", autoIncrement: true });
        usersStore.createIndex("username", "username", { unique: true });
        usersStore.createIndex("password", "password", { unique: false });
    }
};

request.onsuccess = function(event) {
    db = event.target.result;
    console.log("Base de données initialisée.");

    // Ajouter un utilisateur par défaut (seulement pour le test)
    addUser("admin", "1234");
};

request.onerror = function(event) {
    console.error("Erreur lors de l'initialisation de la base de données :", event.target.errorCode);
};

// =========================
// 2. Fonction pour ajouter un utilisateur
// =========================
function addUser(username, password) {
    const transaction = db.transaction(["users"], "readwrite");
    const store = transaction.objectStore("users");

    const user = {
        username: username,
        password: password,
    };

    const request = store.add(user);

    request.onsuccess = function() {
        console.log(`Utilisateur ${username} ajouté.`);
    };

    request.onerror = function(event) {
        console.error("Erreur lors de l'ajout de l'utilisateur :", event.target.errorCode);
    };
}

// =========================
// 3. Gestion de la connexion
// =========================
document.getElementById("login-form").addEventListener("submit", function(event) {
    event.preventDefault(); // Empêche le rechargement de la page

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    const transaction = db.transaction(["users"], "readonly");
    const store = transaction.objectStore("users");
    const index = store.index("username");

    // Recherche l'utilisateur dans la base de données
    const request = index.get(username);

    request.onsuccess = function(event) {
        const user = event.target.result;

        if (user && user.password === password) {
            // Connexion réussie
            localStorage.setItem("loggedIn", "true");
            window.location.href = "panel_admin.html";
        } else {
            // Erreur de connexion
            document.getElementById("error-message").textContent = "Identifiant ou mot de passe incorrect.";
        }
    };

    request.onerror = function() {
        console.error("Erreur lors de la recherche de l'utilisateur.");
    };
});

// =========================
// 4. Déconnexion (pour admin.html)
// =========================
function logout() {
    localStorage.removeItem("loggedIn");
    window.location.href = "index.html"; // Retour à la page de connexion
}
