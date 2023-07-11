from app import app
from app.__init__ import db_connection

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


