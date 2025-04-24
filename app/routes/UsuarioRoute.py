from quart import Blueprint
from app.controllers.UsuarioController import criar_usuario, get_usuarios, atualizar_usuario, deletar_usuario, get_usuario_by_discord_id

usuario_bp = Blueprint('usuario_bp', __name__, url_prefix='/api/usuarios')

@usuario_bp.route('/listar', methods=['GET'])
async def listar():
    return await get_usuarios()

@usuario_bp.route('/listar/usuario/<string:discord_id>', methods=['GET'])
async def listar_usuario(discord_id):
    return await get_usuario_by_discord_id(discord_id)

@usuario_bp.route('/criar', methods=['POST'])
async def criar():
    return await criar_usuario()

@usuario_bp.route('/atualizar/<int:id>', methods=['PUT'])
async def atualizar(id):
    return await atualizar_usuario(id)

@usuario_bp.route('/deletar/<int:id>', methods=['DELETE'])
async def deletar(id):
    return await deletar_usuario(id)