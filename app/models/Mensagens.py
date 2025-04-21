from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app import Base

class Mensagem(Base):
    __tablename__ = 'mensagem'

    id = Column(Integer, primary_key=True)
    discord_id = Column(String(21), ForeignKey('usuario.discord_id'), nullable=False)
    servidor_id = Column(String(21), ForeignKey('servidor.guild_id'), nullable=False)
    conteudo = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    usuario = relationship("Usuario", back_populates="mensagens")
    servidor = relationship("Servidor", back_populates="mensagens")

    def __repr__(self):
        return f'<Mensagem: {self.conteudo}>'

    def to_dict(self):
            return {
                'id': self.id,
                'discord_id': self.discord_id,
                'servidor_id': self.servidor_id,
                'conteudo': self.conteudo,
                'created_at': self.created_at,
                'updated_at': self.updated_at
            }