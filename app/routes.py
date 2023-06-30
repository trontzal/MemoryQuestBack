from app import app, db


@app.route('/')
def index():
    return 'MemoryQuest'

@app.route('/usuarios')
def get_usuarios():
    # Ejemplo de consulta SQL
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    return str(users)