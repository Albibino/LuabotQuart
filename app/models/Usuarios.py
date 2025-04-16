from app import db

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    discord_id = db.Column(db.String(18), unique=True, nullable=False)

    def __repr__(self):
        return (f'<Usuario: {self.nome}>')

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'discord_id': self.discord_id
        }