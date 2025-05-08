from quart import Blueprint
from app.controllers.LogsController import get_logs

logs_bp = Blueprint('logs_bp', __name__, url_prefix='/api/logs')

@logs_bp.route('/listar', methods=['GET'])
async def listar():
    return await get_logs()

