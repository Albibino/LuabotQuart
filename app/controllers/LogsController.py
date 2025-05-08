from quart import request, jsonify, abort
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.Logs import Log
from app import async_session_factory

async def get_logs():
    async with async_session_factory() as session:
        result = await session.execute(select(Log))
        logs = result.scalars().all()
        return jsonify([log.to_dict() for log in logs])