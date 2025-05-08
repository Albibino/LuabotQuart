from quart import Blueprint
from app.controllers.MensagemController import get_mensagens, get_mensagem_by_id, get_mensagens_by_discord_id, get_mensagens_by_guild_id, criar_mensagem, deletar_mensagem, deletar_mensagens_by_discord_id, deletar_mensagens_by_guild_id

mensagem_bp = Blueprint('mensagem_bp', __name__, url_prefix='/api/mensagens')

@mensagem_bp.route('/listar', methods=['GET'])
async def listar():
    return await get_mensagens()

@mensagem_bp.route('/id/<int:id>', methods=['GET'])
async def detalhe(id):
    return await get_mensagem_by_id(id)

@mensagem_bp.route('/usuario/<string:discord_id>', methods=['GET'])
async def por_usuario(discord_id):
    return await get_mensagens_by_discord_id(discord_id)

@mensagem_bp.route('/servidor/<string:servidor_id>', methods=['GET'])
async def por_servidor(servidor_id):
    return await get_mensagens_by_guild_id(servidor_id)

@mensagem_bp.route('/criar', methods=['POST'])
async def criar():
    return await criar_mensagem()

@mensagem_bp.route('/deletar/<int:id>', methods=['DELETE'])
async def deletar(id):
    return await deletar_mensagem(id)

@mensagem_bp.route('/deletar/usuario/<string:discord_id>', methods=['DELETE'])
async def deletar_por_usuario(discord_id):
    return await deletar_mensagens_by_discord_id(discord_id)

@mensagem_bp.route('/deletar/servidor/<string:servidor_id>', methods=['DELETE'])
async def deletar_por_servidor(servidor_id):
    return await deletar_mensagens_by_guild_id(servidor_id)
