from flask import Flask, render_template, request, redirect, session, url_for
import json
import bcrypt  
from start.home import crear_dash_app  # Importamos la función del dashboard  


app = Flask(__name__)
app.secret_key = 'clave_secreta_segura'
crear_dash_app(app)

# Cargar usuarios desde JSON
def load_users():
    with open('usuarios.json', 'r', encoding='utf-8') as f:
        return json.load(f)

users = load_users()


@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')

        if username in users:
            hashed = users[username].encode('utf-8')
            if bcrypt.checkpw(password, hashed):
                session['user'] = username
                return redirect(url_for('dashboard'))
        error = "Usuario o contraseña incorrectos"
    
    return render_template('login.html', error=error)


@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=session['user'])


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
