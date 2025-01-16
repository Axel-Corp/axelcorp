document.getElementById('embedForm').addEventListener('submit', function (e) {
    e.preventDefault();

    const username = document.getElementById('username').value || "Embedify";
    const avatar = document.getElementById('avatar').value || "";
    const title = document.getElementById('title').value;
    const url = document.getElementById('url').value || null;
    const description = document.getElementById('description').value;
    const color = document.getElementById('color').value;
    const image = document.getElementById('image').value;
    const authorName = document.getElementById('authorName').value;
    const authorIcon = document.getElementById('authorIcon').value;
    const fieldTitle = document.getElementById('fieldTitle').value;
    const fieldValue = document.getElementById('fieldValue').value;
    const footer = document.getElementById('footer').value;
    const webhookUrl = document.getElementById('webhookUrl').value;

    // Construction de l'embed
    const embed = {
        username: username,
        avatar_url: avatar,
        embeds: [
            {
                title: title,
                url: url,
                description: description,
                color: parseInt(color.replace("#", ""), 16),
                author: authorName ? {
                    name: authorName,
                    icon_url: authorIcon || null
                } : undefined,
                fields: fieldTitle && fieldValue ? [
                    {
                        name: fieldTitle,
                        value: fieldValue
                    }
                ] : [],
                image: image ? { url: image } : undefined,
                footer: footer ? {
                    text: footer
                } : undefined,
                timestamp: new Date().toISOString()
            }
        ]
    };

    // Aperçu de l'embed
    const preview = document.getElementById('previewContent');
    preview.innerHTML = `
        <h3 style="color: ${color}">${title}</h3>
        <p>${description}</p>
        ${authorName ? `<p><strong>Auteur :</strong> ${authorName}</p>` : ''}
        ${fieldTitle && fieldValue ? `<p><strong>${fieldTitle}:</strong> ${fieldValue}</p>` : ''}
        ${image ? `<img src="${image}" alt="Embed Image" style="max-width: 100%;">` : ''}
        <footer>${footer || "Généré avec Embedify"}</footer>
    `;

    // Envoi au webhook
    fetch(webhookUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(embed)
    })
        .then(response => {
            if (response.ok) {
                alert("Embed envoyé avec succès !");
            } else {
                alert("Erreur lors de l'envoi de l'embed.");
            }
        })
        .catch(error => {
            alert("Erreur : " + error.message);
        });
});
