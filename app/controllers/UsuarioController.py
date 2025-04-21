from quart import request, jsonify, abort
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.Usuarios import Usuario
from app import async_session_factory

async def get_usuarios():
    async with async_session_factory() as session:
        result = await session.execute(select(Usuario))
        usuarios = result.scalars().all()
        return jsonify([usuario.to_dict() for usuario in usuarios])

async def criar_usuario():
    data = await request.get_json()
    
    async with async_session_factory() as session:
        novo = Usuario(**data)
        session.add(novo)
        await session.commit()
        return jsonify({"id": novo.id}), 201

async def atualizar_usuario(id):
    async with async_session_factory() as session:
        result = await session.execute(select(Usuario).filter_by(id=id))
        usuario = result.scalar_one_or_none()

        if usuario is None:
            abort(404, "Usuário não encontrado")

        try:
            data = await request.get_json()

            if 'nome' in data:
                usuario.nome = data['nome']
            if 'email' in data:
                usuario.email = data['email']
            if 'discord_id' in data:
                usuario.discord_id = data['discord_id']

            await session.commit()
            return jsonify(usuario.to_dict())

        except Exception as e:
            await session.rollback()
            return jsonify({"error": str(e)}), 500

async def deletar_usuario(id):
    async with async_session_factory() as session:
        result = await session.execute(select(Usuario).filter_by(id=id))
        usuario = result.scalar_one_or_none()

        if usuario is None:
            abort(404, "Usuário não encontrado")

        try:
            await session.delete(usuario)
            await session.commit()
            return jsonify("Usuário excluído com sucesso"), 200

        except Exception as e:
            await session.rollback()
            return jsonify({"error": str(e)}), 500