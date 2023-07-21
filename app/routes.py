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

from flask import request, jsonify

from flask import request, jsonify

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    usuario = data.get('id_usuario')
    contraseña = data.get('contraseña')

    # Verificar si el usuario existe en la base de datos
    cursor = db_connection.cursor(dictionary=True)
    query = "SELECT * FROM usuarios WHERE id_usuario = %s"
    cursor.execute(query, (usuario,))
    result = cursor.fetchone()
    cursor.close()

    if result:
        # Si el usuario existe, verificar la contraseña
        stored_contraseña = result['contraseña']
        if contraseña == stored_contraseña:
            return jsonify({'message': 'Inicio de sesión exitoso'})
        else:
            return jsonify({'error': 'Credenciales inválidas'}), 401
    else:
        return jsonify({'error': 'Usuario no encontrado'}), 401
