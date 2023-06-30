from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)  # Nombre de usuario, único y obligatorio
    password = db.Column(db.String(100), nullable=False)  # Contraseña, obligatoria

    def __repr__(self):
        return f"User('{self.username}')"
