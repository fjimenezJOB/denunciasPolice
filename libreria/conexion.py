from flask import session
from pymongo import MongoClient


MONGO_URL_ATLAS = 'mongodb+srv://franjimenez:Francisco1231998@develop-0hasi.mongodb.net/test?retryWrites=true&w=majority'

client = MongoClient(MONGO_URL_ATLAS, ssl_cert_reqs=False)

db = client['denunciasPolice']


def loginUser(email):
    """
        Coje el email del usuario y comprueba que este en la base de datos y no este desactivado.
        Devuelve un true o false dependiendo si esta en la base de datos o no y una lista con los datos del usuario con ese email.
    """
    collection = db['users']
    user = {}
    resultados = collection.find(
        {'email': email, 'activo': 1}, {'_id': 0, 'name': 1, 'password': 1, 'email': 1, 'tipo': 1, 'dni': 1})

    for documento in resultados:
        user.update(
            {'email': documento['email'], 'name': documento['name'], 'password': documento['password'], 'dni': documento['dni']})

    if user == '{}':
        noRegistrado = True
    else:
        noRegistrado = False
    return user, noRegistrado


def crearUsuario(nombre, apellido, email, password, dni):
    """
        Primero comprueba que el email no este registrado previamente en la base de datos, tanto si esta desactivado como si no
        Registra los usuarios en la base de datos.
    """
    collection = db['users']
    user = []
    resultados = collection.find({'email': email}, {'_id': 0})

    for documento in resultados:
        user.append(documento['email'])

    if len(user) == 0:
        yaRegistrado = False
    else:
        yaRegistrado = True

    # Si el usuario no existe lo registramos

    if yaRegistrado == False:
        collection.insert(
            {'name': nombre, 'apellidos': apellido, 'email': email, 'password': password, 'activo': 1, 'dni': dni})
    return yaRegistrado


def desactivarUsuario(email):
    """
        Desactiva usuarios
    """
    collection = db['usuarios']
    collection.update_one({'email': email}, {'$set': {'activo': 0}})


def registarDenuncia(email, denuncia, foto, fecha, hora, lugar):
    collection = db['denuncias']
    try:
        collection.insert(
            {'email': email, 'denuncia': denuncia, 'fecha': fecha, 'foto': foto, 'lugar': lugar, 'hora': hora, 'activo': 1})
        error = False
    except:
        error = True
    return error

def sacarDenuncias(email):
    collection = db['denuncias']
    user = {}
    resultados = collection.find(
        {'email': email, 'activo': 1}, {'_id': 0, 'denuncia': 1, 'fecha': 1, 'foto': 1, 'lugar': 1, 'hora': 1})

    for documento in resultados:
        user.update(
            {'denuncia': documento['denuncia'], 'fecha': documento['fecha'], 'foto': documento['foto'], 'lugar': documento['lugar']})

    return user

