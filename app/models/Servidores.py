from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app import Base

class Servidor(Base):
    __tablename__ = 'servidor'

    id = Column(Integer, primary_key=True)
    guild_id = Column(String(21), unique=True, nullable=False)
    nome_servidor = Column(String(100), nullable=True)
    admin_discord_id = Column(String(21), ForeignKey('usuario.discord_id'), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    mensagens = relationship("Mensagem", back_populates="servidor")
    usuario = relationship("Usuario", back_populates="servidores")

    def __repr__(self):
        return f'<Servidor: {self.nome}>'

    def to_dict(self):
        return {
            'id': self.id,
            'guild_id': self.guild_id,
            'nome_servidor': self.nome_servidor,
            'admin_discord_id': self.admin_discord_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
