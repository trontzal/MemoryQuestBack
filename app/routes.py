from app import app
from app.__init__ import db_connection
from flask import request

@app.route('/')
def index():
    return "Hola root"

@app.route('/usuarios')
def get_usuarios():
    cursor = db_connection.cursor()
    query = "SELECT * FROM usuarios"
    cursor.execute(query) 
    usuarios = cursor.fetchall()
    cursor.close()

    return str(usuarios)

@app.route('/usuarios', methods=['POST'])
def add_usuario():
    usuario = request.json.get('id_usuario')
    contraseña = request.json.get('contraseña')

    cursor = db_connection.cursor()
    query = "INSERT INTO usuarios (id_usuario, contraseña) VALUES (%s, %s)"
    values = (usuario, contraseña)
    cursor.execute(query, values)
    db_connection.commit()
    cursor.close()

    return "Usuario creado exitosamente"





