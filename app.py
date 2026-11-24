import os, time
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from config import Config
from bd import init_db
from models import User
from forms import RegistrationForm, LoginForm
import controlador_juegos

app = Flask(__name__)
app.config.from_object(Config)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', app.config['SECRET_KEY'])
app.config['DATABASE_URL'] = os.environ.get('DATABASE_URL', app.config['DATABASE_URL'])

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Inicia sesion para acceder al catalogo de videojuegos.'
login_manager.login_message_category = 'warning'

for _ in range(10):
    try:
        init_db()
        break
    except Exception:
        time.sleep(2)

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('juegos'))
    return render_template('base.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        User.create_user(form.username.data, form.password.data)
        flash('Registro exitoso. Ya puedes iniciar sesion.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_username(form.username.data)
        if user and user.verify_password(form.password.data):
            login_user(user)
            flash(f'Bienvenido, {user.username}!', 'success')
            return redirect(request.args.get('next') or url_for('juegos'))
        flash('Credenciales invalidas.', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesion cerrada correctamente.', 'info')
    return redirect(url_for('login'))

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', username=current_user.username)

@app.route('/juegos')
@login_required
def juegos():
    lista = controlador_juegos.obtener_juegos()
    return render_template('juegos.html', juegos=lista)

@app.route('/agregar_juego')
@login_required
def formulario_agregar_juego():
    return render_template('agregar_juego.html')

@app.route('/guardar_juego', methods=['POST'])
@login_required
def guardar_juego():
    controlador_juegos.insertar_juego(request.form['nombre'], request.form['descripcion'], request.form['precio'])
    return redirect(url_for('juegos'))

@app.route('/formulario_editar_juego/<int:id>')
@login_required
def editar_juego(id):
    juego = controlador_juegos.obtener_juego_por_id(id)
    return render_template('editar_juego.html', juego=juego)

@app.route('/actualizar_juego', methods=['POST'])
@login_required
def actualizar_juego():
    controlador_juegos.actualizar_juego(request.form['nombre'], request.form['descripcion'], request.form['precio'], request.form['id'])
    return redirect(url_for('juegos'))

@app.route('/eliminar_juego', methods=['POST'])
@login_required
def eliminar_juego():
    controlador_juegos.eliminar_juego(request.form['id'])
    return redirect(url_for('juegos'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 80)), debug=False)
