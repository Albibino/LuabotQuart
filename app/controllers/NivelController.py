from quart import request, jsonify, abort
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.Niveis import Nivel
from app import async_session_factory

async def get_niveis():
    async with async_session_factory() as session:
        result = await session.execute(select(Nivel))
        niveis = result.scalars().all()
        return jsonify([nivel.to_dict() for nivel in niveis])

async def get_nivel_by_discord_id(discord_id):
    async with async_session_factory() as session:
        result = await session.execute(select(Nivel).filter_by(discord_id=discord_id))
        niveis = result.scalars().all()
        
        if not niveis:
            abort(404, "Níveis não encontrados para este usuário")
            
        return jsonify([nivel.to_dict() for nivel in niveis])

async def criar_nivel():
    data = await request.get_json()
    
    async with async_session_factory() as session:
        novo = Nivel(**data)
        session.add(novo)
        await session.commit()
        return jsonify({"id": novo.id}), 201

async def atualizar_nivel(id):
    async with async_session_factory() as session:
        result = await session.execute(select(Nivel).filter_by(id=id))
        nivel = result.scalar_one_or_none()

        if nivel is None:
            abort(404, "Nível não encontrado")

        try:
            data = await request.get_json()
            
            if 'discord_id' in data:
                nivel.discord_id = data['discord_id']
            if 'nivel' in data:
                nivel.nivel = data['nivel']
            if 'xp' in data:
                nivel.xp = data['xp']
            
            from datetime import datetime
            nivel.updated_at = datetime.utcnow()

            await session.commit()
            return jsonify(nivel.to_dict())

        except Exception as e:
            await session.rollback()
            return jsonify({"error": str(e)}), 500

async def deletar_nivel_by_id(discord_id):
    async with async_session_factory() as session:
        result = await session.execute(select(Nivel).filter_by(discord_id=discord_id))
        niveis = result.scalars().all()

        if not niveis:
            abort(404, "Níveis não encontrados para este usuário")

        try:
            for nivel in niveis:
                await session.delete(nivel)
            await session.commit()
            return jsonify(f"Níveis do usuário com Discord ID {discord_id} excluídos com sucesso"), 200

        except Exception as e:
            await session.rollback()
            return jsonify({"error": str(e)}), 500
