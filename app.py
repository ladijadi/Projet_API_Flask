from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Liste des utilisateurs stockée en mémoire (pour simplifier)
users = [
    {
        "first_name": "Alice",
        "last_name": "Dupont",
        "email": "alice.dupont@example.com",
        "phone": "+33 6 12 34 56 78"
    },
    {
        "first_name": "Bob",
        "last_name": "Martin",
        "email": "bob.martin@example.com",
        "phone": "+33 6 23 45 67 89"
    },
        {
        "first_name": "Claire",
        "last_name": "Lemoine",
        "email": "claire.lemoine@example.com",
        "phone": "+33 6 34 56 78 90"
    },
    {
        "first_name": "David",
        "last_name": "Durand",
        "email": "david.durand@example.com",
        "phone": "+33 6 45 67 89 01"
    },
    {
        "first_name": "Eva",
        "last_name": "Moreau",
        "email": "eva.moreau@example.com",
        "phone": "+33 6 56 78 90 12"
    }
]
# Route pour afficher le formulaire et ajouter un utilisateur
@app.route('/add', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        # Récupérer les données du formulaire
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        phone = request.form.get('phone')

        # Vérifier que tous les champs sont remplis
        if not first_name or not last_name or not email or not phone:
            return "Tous les champs sont requis", 400

        # Ajouter l'utilisateur à la liste
        users.append({
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "phone": phone
        })
        # Rediriger vers la liste des utilisateurs
        return redirect(url_for('list_users'))

    return render_template('add_user.html')

# Route pour afficher la liste des utilisateurs
@app.route('/users', methods=['GET'])
def list_users():
    return render_template('list_users.html', users=users)

if __name__ == '__main__':
    app.run(debug=True)