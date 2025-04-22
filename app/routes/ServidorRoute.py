from quart import Blueprint
from app.controllers.ServidorController import get_servidores, criar_servidor, atualizar_servidor, deletar_servidor

servidor_bp = Blueprint('servidor_bp', __name__, url_prefix='/api/servidores')

@servidor_bp.route('/listar', methods=['GET'])
async def listar():
    return await get_servidores()

@servidor_bp.route('/criar', methods=['POST'])
async def criar():
    return await criar_servidor()

@servidor_bp.route('/atualizar/<int:id>', methods=['PUT'])
async def atualizar(id):
    return await atualizar_servidor(id)

@servidor_bp.route('/deletar/<int:id>', methods=['DELETE'])
async def deletar(id):
    return await deletar_servidor(id)