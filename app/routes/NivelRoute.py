from quart import Blueprint
from app.controllers.NivelController import get_niveis, get_nivel_by_discord_id, criar_nivel, atualizar_nivel, deletar_nivel_by_id

nivel_bp = Blueprint('nivel_bp', __name__, url_prefix='/api/niveis')

@nivel_bp.route('/listar', methods=['GET'])
async def listar():
    return await get_niveis()

@nivel_bp.route('/usuario/<string:discord_id>', methods=['GET'])
async def por_usuario(discord_id):
    return await get_nivel_by_discord_id(discord_id)

@nivel_bp.route('/criar', methods=['POST'])
async def criar():
    return await criar_nivel()

@nivel_bp.route('/atualizar/<int:id>', methods=['PUT'])
async def atualizar(id):
    return await atualizar_nivel(id)

@nivel_bp.route('/deletar/usuario/<string:discord_id>', methods=['DELETE'])
async def deletar_por_id(discord_id):
    return await deletar_nivel_by_id(discord_id)
