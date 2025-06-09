from quart import Quart
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
    app = Quart(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+asyncpg://postgres:postgres@localhost:5432/luabotdb"
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

    from app.routes.UsuarioRoute import usuario_bp
    from app.routes.ServidorRoute import servidor_bp
    from app.routes.NivelRoute import nivel_bp
    from app.routes.MensagemRoute import mensagem_bp
    from app.routes.LogsRoute import logs_bp
    app.register_blueprint(usuario_bp)
    app.register_blueprint(servidor_bp)
    app.register_blueprint(nivel_bp)
    app.register_blueprint(mensagem_bp)
    app.register_blueprint(logs_bp)

    return app
