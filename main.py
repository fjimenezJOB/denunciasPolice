from flask import Flask, render_template, redirect, request, session


app = Flask(__name__)

app.secret_key = 'secret_key'

@app.route('/')
def home():
    if session:
        return render_template('home.html')
    else:
        return redirect('login')
    return render_template('login.html')

@app.route('/login')
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
                session['tipo'] = user['tipo']
                return redirect('menu')
        else:
            error = True
            return render_template('login.html', error=error, **content)
    return render_template('login.html', **content)

if __name__ == "__main__":
    app.run('0.0.0.0', 8080, debug= True)