from flask import Flask, render_template, redirect, request, session
from werkzeug.utils import secure_filename
from libreria.conexion import *
import datetime
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/img/uploads/'
app.secret_key = 'secret_key'


@app.route('/')
def home():
    if session:
        return redirect('index')
    return redirect('login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    content = {
        'titulo': 'Inicia Sesión o Regístrate',
        'subtitulo': 'Gracias por confiar en nosotros.'
    }

    if session:
        return redirect('index')

    if request.method == 'POST':
        email = request.form.get('email')
        contra = request.form.get('password')
        user, noRegistrado = loginUser(email)

        if user and noRegistrado == False:
            if user['email'] == email and user['password'] == contra:
                session['name'] = user['name']
                session['email'] = email
                session['dni'] = user['dni']
                return redirect('index')
        else:
            error = True
            return render_template('login.html', error=error, **content)
    return render_template('login.html', **content)

@app.route('/index', methods=['GET', 'POST'])
def index():
    context = {
        'titulo' : 'Menu',
        'subtitulo' : 'Opciones'
    }
    if session:
        return render_template('index.html', **context)
    else:
        return redirect('login')

@app.route('/denuncia', methods=['GET', 'POST'])
def denuncia():
    error = False
    if session:
        if request.method == 'POST':
            foto = request.files['foto']
            filename = secure_filename(foto.filename)
            foto.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            denuncia = request.form.get('denuncia')
            lugar =  request.form.get('lugar')
            fecha = request.form.get('fecha')
            hora = request.form.get('hora')
            foto = request.form.get('foto')
            error = registarDenuncia(session['email'], denuncia, filename, fecha, hora, lugar)
        context = {
            'titulo' : 'Rellena el formulario para registrar tu denuncia.',
            'error' : error
        }
        
    else:
        return redirect('login')
    return render_template('denuncia.html', **context)


@app.route('/listar')
def listar():
    if session:
        denuncias = sacarDenuncias(session['email'])
        context = {
            'titulo' : 'Lista de denuncias',
            'subtitulo' : 'Tus Denuncias'
        }
        return render_template('listar.html', denuncias=denuncias, **context)
    else:
        return redirect('login')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """
        Registra usuarios en la base de datos y comprueba que ese usuario no este.
    """
    context = {
        'titulo' : 'Registro de Usuarios',
        'subtitulo' : 'Gracias por confiar en nosotros.'
    }
    if request.method == 'POST':
        nombre = request.form.get('name')
        apellido = request.form.get('apellidos')
        email = request.form.get('email')
        password = request.form.get('password')
        dni = request.form.get('dni')
        yaRegistrado = crearUsuario(
            nombre, apellido, email, password, dni)
        if yaRegistrado:
            error = True
            return render_template('register.html', error=error, **context)
        else:
            return redirect('index')
    return render_template('register.html', **context)

@app.route('/desactivar', methods=['GET', 'POST'])
def desactivar():
    if request.method == 'POST':
        denuncia = request.form.get('denuncia')
        desactivarDenuncia(session['email'], denuncia)
    return redirect('listar')

@app.route('/salir')
def salir():
    session.clear()
    return redirect('login')


if __name__ == "__main__":
    app.run('0.0.0.0', 8080, debug=True)