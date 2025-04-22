from quart import request, jsonify, abort
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.Mensagens import Mensagem
from app import async_session_factory

async def get_mensagens():
    async with async_session_factory() as session:
        result = await session.execute(select(Mensagem))
        mensagens = result.scalars().all()
        return jsonify([mensagem.to_dict() for mensagem in mensagens])

async def get_mensagem_by_id(id):
    async with async_session_factory() as session:
        result = await session.execute(select(Mensagem).filter_by(id=id))
        mensagem = result.scalar_one_or_none()
        
        if mensagem is None:
            abort(404, "Mensagem não encontrada")
            
        return jsonify(mensagem.to_dict())

async def get_mensagens_by_discord_id(discord_id):
    async with async_session_factory() as session:
        result = await session.execute(select(Mensagem).filter_by(discord_id=discord_id))
        mensagens = result.scalars().all()
        
        if not mensagens:
            abort(404, "Mensagens não encontradas para este usuário")
            
        return jsonify([mensagem.to_dict() for mensagem in mensagens])

async def get_mensagens_by_guild_id(servidor_id):
    async with async_session_factory() as session:
        result = await session.execute(select(Mensagem).filter_by(servidor_id=servidor_id))
        mensagens = result.scalars().all()
        
        if not mensagens:
            abort(404, "Mensagens não encontradas para este servidor")
            
        return jsonify([mensagem.to_dict() for mensagem in mensagens])

async def criar_mensagem():
    data = await request.get_json()
    
    async with async_session_factory() as session:
        nova = Mensagem(**data)
        session.add(nova)
        await session.commit()
        return jsonify({"id": nova.id}), 201

async def deletar_mensagem(id):
    async with async_session_factory() as session:
        result = await session.execute(select(Mensagem).filter_by(id=id))
        mensagem = result.scalar_one_or_none()

        if mensagem is None:
            abort(404, "Mensagem não encontrada")

        try:
            await session.delete(mensagem)
            await session.commit()
            return jsonify("Mensagem excluída com sucesso"), 200

        except Exception as e:
            await session.rollback()
            return jsonify({"error": str(e)}), 500

async def deletar_mensagens_by_discord_id(discord_id):
    async with async_session_factory() as session:
        result = await session.execute(select(Mensagem).filter_by(discord_id=discord_id))
        mensagens = result.scalars().all()

        if not mensagens:
            abort(404, "Mensagens não encontradas para este usuário")

        try:
            for mensagem in mensagens:
                await session.delete(mensagem)
            await session.commit()
            return jsonify(f"Mensagens do usuário com Discord ID {discord_id} excluídas com sucesso"), 200

        except Exception as e:
            await session.rollback()
            return jsonify({"error": str(e)}), 500

async def deletar_mensagens_by_guild_id(servidor_id):
    async with async_session_factory() as session:
        result = await session.execute(select(Mensagem).filter_by(servidor_id=servidor_id))
        mensagens = result.scalars().all()

        if not mensagens:
            abort(404, "Mensagens não encontradas para este servidor")

        try:
            for mensagem in mensagens:
                await session.delete(mensagem)
            await session.commit()
            return jsonify(f"Mensagens do servidor com ID {servidor_id} excluídas com sucesso"), 200

        except Exception as e:
            await session.rollback()
            return jsonify({"error": str(e)}), 500
