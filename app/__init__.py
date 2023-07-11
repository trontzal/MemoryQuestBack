from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)
app.config['SECRET_KEY'] = 'claveSecreta'

#configuracion bbdd
db_config ={
    'user' : 'root',
    'password' : 'usuario',
    'host' : 'localhost',
    'database' : 'memoryquest'
}

db_connection = mysql.connector.connect(**db_config)
db_cursor =db_connection.cursor(dictionary=True)

@app.teardown_appcontext
def close_db_connection(error):
    db_cursor.close()
    db_connection.close()

from app import routes