from flask import Blueprint
from app.controllers.UsuarioController import criar_usuario, get_usuarios, atualizar_usuario, deletar_usuario

usuario_bp = Blueprint('usuario_bp', __name__, url_prefix='/usuarios')

usuario_bp.route('/listar', methods=['GET'])(get_usuarios)
usuario_bp.route('/criar',methods=['POST'])(criar_usuario)
usuario_bp.route('/atualizar/<int:id>', methods=['PUT'])(atualizar_usuario)
usuario_bp.route('/deletar/<int:id>', methods=['DELETE'])(deletar_usuario)