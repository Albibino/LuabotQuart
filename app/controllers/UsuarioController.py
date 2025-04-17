from flask import request, jsonify, abort
from app import db
from app.models.Usuarios import Usuario

def get_usuarios():
    usuarios = Usuario.query.all()
    return jsonify(list(usuario.to_dict() for usuario in usuarios))

def criar_usuario():
    data = request.get_json()
    novo = Usuario(**data)
    db.session.add(novo)
    db.session.commit()
    return jsonify({"id": novo.id}), 201

def atualizar_usuario(id):

    usuario = Usuario.query.get(id)

    if usuario is None:
        abort(404, "Usuário não encontrado")

    try:

        data = request.get_json()

        if 'nome' in data:
            usuario.nome = data['nome']
        if 'email' in data:
            usuario.email = data['email']
        if 'discord_id' in data:
            usuario.discord_id = data['discord_id']

        db.session.commit()
        return jsonify(usuario.to_dict())

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

def deletar_usuario(id):

    usuario = Usuario.query.get(id)

    if usuario is None:
        abort(404, "Usuário não encontrado")

    try:
        
        db.session.delete(usuario)
        db.session.commit()
        return jsonify("Usuário excluído com sucesso"),200

    except Exception as e:

        db.session.rollback()
        return jsonify({"error": str(e)}), 500