from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app import Base

class Nivel(Base):
    __tablename__ = 'nivel'

    id = Column(Integer, primary_key=True)
    discord_id = Column(String(21), ForeignKey('usuario.discord_id'), nullable=False)
    nivel = Column(Integer, nullable=False, default=1)
    xp = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    usuario = relationship("Usuario", back_populates="niveis")

    def __repr__(self):
        return (f'<Usuario: {self.discord_id} Nivel: {self.nivel}>')

    def to_dict(self):
        return {
            'id': self.id,
            'discord_id': self.discord_id,
            'nivel': self.nivel,
            'xp': self.xp,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }