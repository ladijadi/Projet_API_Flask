from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['DEBUG'] = True
app.secret_key = 'your_secret_key'  # Nécessaire pour gérer les sessions

# Initialisation d'une liste d'utilisateurs avec un mot de passe hashé
users_list = [
    {
        'id': 1,
        'nom': 'seck',
        'prenom': 'cheikh',
        'username': 'tidiane',
        'password': generate_password_hash('password123')  # Mot de passe hashé
    },
    {
        'id': 2,
        'nom': 'alpha',
        'prenom': 'diagne',
        'username': 'omega',
        'password': generate_password_hash('half_life')  # Mot de passe hashé
    }
]

# Route pour l'inscription
@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nom = request.form['nom']
        prenom = request.form['prenom']
        username = request.form['username']
        password = request.form['password']

        # Vérifier si l'utilisateur existe déjà
        existing_user = next((user for user in users_list if user['username'] == username), None)
        if existing_user:
            return "Le nom d'utilisateur est déjà pris", 400

        # Ajouter l'utilisateur avec un mot de passe hashé
        new_user = {
            'id': users_list[-1]['id'] + 1,
            'nom': nom,
            'prenom': prenom,
            'username': username,
            'password': generate_password_hash(password)
        }
        users_list.append(new_user)

        return redirect(url_for('login'))

    return render_template('register.html')

# Route pour la connexion
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Recherche de l'utilisateur correspondant
        user = next((user for user in users_list if user['username'] == username), None)
        
        if user and check_password_hash(user['password'], password):
            # Authentification réussie, on stocke l'utilisateur dans la session
            session['user_id'] = user['id']
            return redirect(url_for('index'))
        else:
            return "Identifiants invalides", 401  # Erreur de connexion

    return render_template('login.html')

# Route pour la déconnexion
@app.route("/logout")
def logout():
    # Déconnexion : on supprime l'utilisateur de la session
    session.pop('user_id', None)
    return redirect(url_for('index'))

# Page d'accueil
@app.route("/")
@app.route("/index")
def index():
    return "Bienvenue sur la page d'accueil !"

if __name__ == "__main__":
    app.run()
