from quart import request, jsonify, abort
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.Servidores import Servidor
from app import async_session_factory

async def get_servidores():
    async with async_session_factory() as session:
        result = await session.execute(select(Servidor))
        servidores = result.scalars().all()
        return jsonify([servidor.to_dict() for servidor in servidores])

async def criar_servidor():
    data = await request.get_json()
    
    async with async_session_factory() as session:
        novo = Servidor(**data)
        session.add(novo)
        await session.commit()
        return jsonify({"id": novo.id}), 201

async def atualizar_servidor(id):
    async with async_session_factory() as session:
        result = await session.execute(select(Servidor).filter_by(id=id))
        servidor = result.scalar_one_or_none()

        if servidor is None:
            abort(404, "Servidor não encontrado")

        try:
            data = await request.get_json()

            if 'guild_id' in data:
                servidor.guild_id = data['guild_id']
            if 'nome_servidor' in data:
                servidor.nome_servidor = data['nome_servidor']
            if 'admin_discord_id' in data:
                servidor.admin_discord_id = data['admin_discord_id']
            
            from datetime import datetime
            servidor.updated_at = datetime.utcnow()

            await session.commit()
            return jsonify(servidor.to_dict())

        except Exception as e:
            await session.rollback()
            return jsonify({"error": str(e)}), 500

async def deletar_servidor(id):
    async with async_session_factory() as session:
        result = await session.execute(select(Servidor).filter_by(id=id))
        servidor = result.scalar_one_or_none()

        if servidor is None:
            abort(404, "Servidor não encontrado")

        try:
            await session.delete(servidor)
            await session.commit()
            return jsonify("Servidor excluído com sucesso"), 200

        except Exception as e:
            await session.rollback()
            return jsonify({"error": str(e)}), 500