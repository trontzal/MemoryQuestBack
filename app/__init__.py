from flask import Flask
import mysql.connector
from config.config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret_key'

# Configuración de la base de datos
db = mysql.connector.connect(
    host=DB_HOST,
    port=DB_PORT,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME
)

# Registra las rutas y otros componentes de la aplicación aquí
from app import routes
