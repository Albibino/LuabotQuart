from sqlalchemy import Column, Integer, String, LargeBinary, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app import Base

class Foto(Base):
    __tablename__ = 'foto'

    id = Column(Integer, primary_key=True)
    nome = Column(String(255), nullable=False)
    tipo_mime = Column(String(50), nullable=False)
    tamanho = Column(Integer, nullable=False)
    dados = Column(LargeBinary, nullable=False)
    usuario_id = Column(Integer, ForeignKey('usuario.id'), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    usuario = relationship("Usuario", back_populates="fotos")

    def __repr__(self):
        return f'<Foto: {self.nome}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'tipo_mime': self.tipo_mime,
            'tamanho': self.tamanho,
            'usuario_id': self.usuario_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }