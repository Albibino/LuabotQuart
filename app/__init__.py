from flask import Flask
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

async_engine = create_async_engine(
    "postgresql+asyncpg://postgres:postgres@localhost:5432/luabotdb",
    echo=True,
)

async_session_factory = async_sessionmaker(
    async_engine,
    expire_on_commit=False,
    class_=AsyncSession
)

async def get_async_session():
    async with async_session_factory() as session:
        yield session

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+asyncpg://postgres:postgres@localhost:5432/luabotdb"

    from app.routes.UsuarioRoute import usuario_bp
    app.register_blueprint(usuario_bp)

    return app