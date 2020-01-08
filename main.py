from flask import Flask, render_template, redirect, request, session
from libreria.conexion import *
import datetime

app = Flask(__name__)

app.secret_key = 'secret_key'


@app.route('/')
def home():
    if session:
        return render_template('index.html')
    else:
        return redirect('login')
    return render_template('login.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    content = {
        'titulo': 'Inicia Sesión',
        'subtitulo': 'Login'
    }

    if request.method == 'POST':
        email = request.form.get('email')
        contra = request.form.get('password')

        user, noRegistrado = loginUser(email)

        if user and noRegistrado == False:
            if user['email'] == email and user['password'] == contra:
                session['name'] = user['name']
                session['email'] = email
                session['FNI'] = user['dni']
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
    return render_template('index.html', **context)

@app.route('/denuncia', methods=['GET', 'POST'])
def denuncia():
    error = False
    if request.method == 'POST':
        denuncia = request.form.get('denuncia')
        lugar =  request.form.get('lugar')
        fecha = request.form.get('fecha')
        hora = request.form.get('hora')
        foto = request.form.get('foto')
        error = registarDenuncia(session['email'], denuncia, foto, fecha, hora, lugar)

    context = {
        'titulo' : 'Rellena el formulario para registrar tu denuncia.',
        'error' : error
    }

    return render_template('denuncia.html', **context)

@app.route('/listar')
def listar():
    denuncias = sacarDenuncias(session['email'])
    context = {
        'titulo' : 'Lista de denuncias',
        'subtitulo' : 'Tus Denuncias'
    }
    return render_template('listar.html', denuncias=denuncias)


@app.route('/register', methods=['GET', 'POST'])
def register():
    """
        Registra usuarios en la base de datos y comprueba que ese usuario no este.
    """

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
            return render_template('register.html', error=error)
        else:
            return redirect('login')

    return render_template('register.html')

@app.route('/salir')
def salir():
    session.clear()
    return redirect('login')


if __name__ == "__main__":
    app.run('0.0.0.0', 8080, debug=True)