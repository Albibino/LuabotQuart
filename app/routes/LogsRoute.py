from quart import Blueprint
from app.controllers.LogsController import get_logs

logs_bp = Blueprint('logs_bp', __name__, url_prefix='/api/logs')

@logs_bp.route('/listar', methods=['GET'])
async def listar():
<<<<<<< HEAD
    return await get_logs()
=======
    return await get_logs()
>>>>>>> 43a83a2d35896ed7055314e6df7ed9d9c32452a4
