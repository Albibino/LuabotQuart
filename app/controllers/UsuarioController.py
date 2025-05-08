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

async def get_usuario_by_discord_id(discord_id):
    async with async_session_factory() as session:
        result = await session.execute(select(Usuario).filter_by(discord_id=discord_id))
        usuario = result.scalar_one_or_none()
        if usuario is None:
            abort(404, "Usuario não encontrado")
        return jsonify(usuario.to_dict())

async def criar_usuario():
    data = await request.get_json()
    
    async with async_session_factory() as session:
        try:
            novo = Usuario(**data)
            session.add(novo)
            await session.flush()

            from app.models.Niveis import Nivel
            novo_nivel = Nivel(
                discord_id=novo.discord_id
            )
            session.add(novo_nivel)
            await session.commit()
            return jsonify({"id": novo.id, "nivel_id": novo_nivel.id}), 201
            
        except Exception as e:
            await session.rollback()
            return jsonify({"error": str(e)}), 500


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

            from datetime import datetime
            usuario.updated_at = datetime.utcnow()

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
            from app.models.Niveis import Nivel
            discord_id = usuario.discord_id
            niveis_result = await session.execute(select(Nivel).filter_by(discord_id=discord_id))
            niveis = niveis_result.scalars().all()
            for nivel in niveis:
                await session.delete(nivel)
            await session.delete(usuario)
            await session.commit()
            return jsonify("Usuário excluído com sucesso"), 200

        except Exception as e:
            await session.rollback()
            return jsonify({"error": str(e)}), 500