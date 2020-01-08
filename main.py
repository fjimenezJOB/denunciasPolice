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
        'titulo':'Rellena el formulario para registrar tu denuncia.'
    }
    if request.method == 'POST':
        denuncia = request.POST.get('denuncia')
        lugar =  request.POST.get('lugar')
        fecha = request.POST.get('fecha')
        hora = request.POST.get('hora')
        foto = request.POST.get('foto')

    return render_template('index.html', **context)

@app.route('/denuncia', methods=['GET', 'POST'])
def denuncia():
    context = {
        'titulo' : 'Rellena el formulario para registrar tu denuncia.'
    }
    return render_template('denuncia.html', **context) 


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