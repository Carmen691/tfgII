from flask import Flask, render_template, request, redirect, session, url_for
import json
import bcrypt  
from start.home import crear_dash_app  # Importamos la función del dashboard  
import data.querys as dq

app = Flask(__name__)
app.secret_key = 'clave_secreta_segura'
crear_dash_app(app)
@app.before_request
def proteger_dash():
    # Si la ruta empieza con /dash y el usuario no está logueado, redirige a login
    if request.path.startswith('/dash') and 'user' not in session:
        return redirect(url_for('login'))


@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')

        if dq.existe_usuario(username):
            passwd = dq.obtener_pwd(username).encode('utf-8')
            if bcrypt.checkpw(password, passwd):
                session['user'] = username
                session['admin'] = dq.obtener_admin(username)
                return redirect(url_for('dashboard'))
        error = "Usuario o contraseña incorrectos"
    
    return render_template('login.html', error=error)


@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    return redirect('/dash')
    #return render_template('dashboard.html', username=session['user'])


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
