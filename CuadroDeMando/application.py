from datetime import timedelta

from flask import Flask, render_template, request, redirect, session, url_for
import json
import bcrypt  
from start.home import crear_dash_app  # Importamos la función del dashboard  
import data.querys as dq

application = Flask(__name__)
application.secret_key = 'clave_secreta_segura'
application.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
crear_dash_app(application)
@application.before_request
def proteger_dash():
    if '/_dash-' in request.path:
        return None
    if request.path.startswith('/dash') and 'user' not in session:
        return redirect(url_for('login'))


@application.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')

        if dq.existe_usuario(username):
            passwd = dq.obtener_pwd(username)
            if bcrypt.checkpw(password, passwd.encode('utf-8')):
                session['user'] = username
                session['admin'] = dq.obtener_admin(username)
                session.permanent = True
                dq.registrar_auditoria(username, 'LOGIN', 'El usuario se ha logado correctamente')
                return redirect(url_for('dashboard'))
        error = "Usuario o contraseña incorrectos"
    
    return render_template('login.html', error=error)


@application.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    return redirect('/dash')


@application.route('/logout')
def logout():
    dq.registrar_auditoria(session.get('user'), 'LOGOUT', 'El usuario ha cerrado la sesión')
    session.pop('user', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    
    application.run(debug=True)
