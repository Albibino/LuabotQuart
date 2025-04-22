from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app import Base

class Usuario(Base):
    __tablename__ = 'usuario'

    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    admin = Column(Boolean, nullable=False, default=False)
    discord_id = Column(String(21), unique=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    servidores = relationship("Servidor", back_populates="usuario")
    mensagens = relationship("Mensagem", back_populates="usuario")
    niveis = relationship("Nivel", back_populates="usuario")

    def __repr__(self):
        return (f'<Usuario: {self.nome}>')

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'discord_id': self.discord_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }