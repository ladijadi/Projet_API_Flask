from flask import Flask, render_template, request, redirect, session, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Utilise une clé secrète plus complexe en production

# Simuler une base de données des utilisateurs (dictionnaire) pour la partie authentification
users_db = {
    "john@example.com": {
        "name": "John Doe",
        "password": generate_password_hash("mypassword")  # Mot de passe hashé
    }
}

# Route pour s'inscrire et ajouter un utilisateur avec un mot de passe hashé
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        name = request.form['name']
        password = request.form['password']

        # Vérifier si l'utilisateur existe déjà
        if email in users_db:
            flash('Email déjà utilisé.')
            return redirect(url_for('register'))

        # Hashage du mot de passe et ajout à la base de données simulée
        users_db[email] = {
            "name": name,
            "password": generate_password_hash(password)
        }
        flash('Utilisateur enregistré avec succès. Connectez-vous.')
        return redirect(url_for('login'))

    return render_template('register.html')

# Route pour se connecter et créer une session utilisateur
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Vérification des identifiants
        if email in users_db and check_password_hash(users_db[email]['password'], password):
            session['user'] = email  # Stocker l'email dans la session pour indiquer que l'utilisateur est connecté
            flash('Connexion réussie.')
            return redirect(url_for('dashboard'))
        else:
            flash('Identifiants incorrects.')
    
    return render_template('login.html')

# Route pour déconnexion
@app.route('/logout')
def logout():
    session.pop('user', None)  # Supprimer l'utilisateur de la session
    flash('Déconnexion réussie.')
    return redirect(url_for('login'))

# Tableau de bord réservé aux utilisateurs connectés
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        flash('Vous devez être connecté pour accéder au tableau de bord.')
        return redirect(url_for('login'))
    
    user_email = session['user']
    return f'Bienvenue {users_db[user_email]["name"]} ! <a href="/logout">Déconnexion</a>'

if __name__ == '__main__':
    app.run(debug=True)
