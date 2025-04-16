from app import db

class Servidor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    guild_id = db.Column(db.String(18), unique=True, nullable=False)
    nome = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f'<Servidor: {self.nome}>'
