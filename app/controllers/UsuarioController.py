from flask import request, jsonify, abort
from app import db
from app.models.Usuarios import Usuario

def criar_usuario():
    data = request.get_json()
    novo = Usuario(**data)
    db.session.add(novo)
    db.session.commit()
    return jsonify({"id": novo.id}), 201

def get_usuario(id):
    usuario = Usuario.query.get(id)
    if usuario is None:
        abort(404, "Usuário não encontrado")
    return jsonify(usuario.to_dict())