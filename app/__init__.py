from flask import Flask, jsonify, request
import mysql.connector
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'claveSecreta'

#configuracion bbdd
db_config ={
    'user' : 'root',
    'password' : 'Uz6Tc26jqMT7lPo8GMnB',
    'host' : 'containers-us-west-115.railway.app',
    'database' : 'railway',
    'port' : 6714
}

try:
    db_connection = mysql.connector.connect(**db_config)
    db_cursor =db_connection.cursor(dictionary=True)
    print("Conexion exitosa")

except mysql.connector.Error as error:
    print("Conexion a la base de datos fallida: {error}")

@app.teardown_appcontext
def close_db_connection(error):
    db_cursor.close()
    db_connection.close()

from app import routes