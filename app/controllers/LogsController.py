from quart import request, jsonify, abort
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.Logs import Log
from app import async_session_factory

async def get_logs():
    async with async_session_factory() as session:
        result = await session.execute(select(Log))
        logs = result.scalars().all()
<<<<<<< HEAD
        return jsonify([log.to_dict() for log in logs])
=======
        return jsonify([log.to_dict() for log in logs])

    
>>>>>>> 43a83a2d35896ed7055314e6df7ed9d9c32452a4
