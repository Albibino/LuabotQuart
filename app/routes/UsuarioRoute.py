from flask import Blueprint
from app.controllers.UsuarioController import criar_usuario, get_usuario

usuario_bp = Blueprint('usuario_bp', __name__, url_prefix='/usuarios')

usuario_bp.route('/criar',methods=['POST'])(criar_usuario)
usuario_bp.route('/<int:id>',methods=['GET'])(get_usuario)