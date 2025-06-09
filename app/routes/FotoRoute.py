from quart import Blueprint
from app.controllers.FotoController import (
    criar_foto,
    get_fotos,
    get_foto_by_id,
    download_foto,
    atualizar_foto,
    deletar_foto,
    get_fotos_by_usuario,
    deletar_fotos_by_usuario
)

foto_bp = Blueprint('foto', __name__, url_prefix='/api/fotos')

@foto_bp.route('', methods=['POST'])
async def create_foto():
    return await criar_foto()

@foto_bp.route('', methods=['GET'])
async def get_all_fotos():
    return await get_fotos()

@foto_bp.route('/<int:foto_id>', methods=['GET'])
async def get_foto(foto_id):
    return await get_foto_by_id(foto_id)

@foto_bp.route('/<int:foto_id>/download', methods=['GET'])
async def download_image(foto_id):
    return await download_foto(foto_id)

@foto_bp.route('/<int:foto_id>', methods=['PUT'])
async def update_foto(foto_id):
    return await atualizar_foto(foto_id)

@foto_bp.route('/<int:foto_id>', methods=['DELETE'])
async def delete_foto(foto_id):
    return await deletar_foto(foto_id)

@foto_bp.route('/usuario/<int:usuario_id>', methods=['GET'])
async def get_fotos_usuario(usuario_id):
    return await get_fotos_by_usuario(usuario_id)

@foto_bp.route('/usuario/<int:usuario_id>', methods=['DELETE'])
async def delete_fotos_usuario(usuario_id):
    return await deletar_fotos_by_usuario(usuario_id)
