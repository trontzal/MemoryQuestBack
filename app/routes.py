from app import app
from app.__init__ import db_connection
from flask import request, jsonify

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

    # Verificar si el usuario ya existe
    query = "SELECT COUNT(*) FROM usuarios WHERE id_usuario = %s"
    cursor.execute(query, (usuario,))
    count = cursor.fetchone()[0]

    if count > 0:
        # Si el usuario ya existe, retornar un error
        return "El usuario ya existe. Por favor, elige otro nombre de usuario.", 409

    # Insertar el nuevo usuario en la base de datos
    query = "INSERT INTO usuarios (id_usuario, contraseña) VALUES (%s, %s)"
    values = (usuario, contraseña)
    cursor.execute(query, values)
    db_connection.commit()
    cursor.close()

    return "Usuario creado exitosamente", 201

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

@app.route('/crear_juego', methods=['POST'])
def crear_juego():
    try:
        id_juego = request.json.get('id_juego')
        nombre_juego = request.json.get('nombre_juego')

        cursor = db_connection.cursor()

        # Consulta SQL para insertar el juego en la tabla juegos
        query = "INSERT INTO juegos (id_juego, nombre) VALUES (%s, %s)"
        values = (id_juego, nombre_juego)
        cursor.execute(query, values)

        db_connection.commit()
        cursor.close()
        db_connection.close()

        return jsonify({"message": "Juego creado exitosamente"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/agregar_puntuacion', methods=['POST'])
def agregar_puntuacion():
    try:
        puntuacion = request.json.get('puntuacion')
        id_usuario = request.json.get('id_usuario')
        id_juego = request.json.get('id_juego')

        cursor = db_connection.cursor()

        query = "INSERT INTO puntuaciones (puntuacion, id_usuario, id_juego) VALUES (%s, %s, %s)"
        values = (puntuacion, id_usuario, id_juego)
        cursor.execute(query, values)

        db_connection.commit()
        cursor.close()

        return jsonify({"message": "Puntuación agregada exitosamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/puntuaciones')
def ver_puntuaciones():
    cursor = db_connection.cursor()
    query = "SELECT * FROM puntuaciones"
    cursor.execute(query) 
    puntos = cursor.fetchall()
    cursor.close()

    return str(puntos)

@app.route('/grafico/<string:id_juego>', methods=['GET'])
def obtener_puntuaciones(id_juego):
    try:
        cursor = db_connection.cursor()
        query = "SELECT puntuacion, COUNT(*) AS repeticiones FROM puntuaciones WHERE id_juego = %s GROUP BY puntuacion"
        cursor.execute(query, (id_juego,))
        puntuaciones = cursor.fetchall()
        cursor.close()

        grafica = []
        for dato in puntuaciones:
            grafica.append({
                'x': dato[0],
                'y': dato[1]
            })

        return jsonify(grafica)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

