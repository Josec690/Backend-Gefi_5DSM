from flask import Blueprint, request, jsonify
from app.controllers.market_controller import MarketController
from app.database.connection import get_db
from app.middlewares.auth_middleware import token_required
from flask import g

market_bp = Blueprint('market', __name__, url_prefix='/market')

@market_bp.route('/stock/<symbol>', methods=['GET'])
@token_required
def get_stock(symbol):
    """Obter dados de ação"""
    try:
        db = get_db()
        controller = MarketController(db)
        user_id = str(g.user["_id"])
        return controller.get_stock_data(symbol, user_id)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@market_bp.route('/tesouro-direto', methods=['GET'])
@token_required
def get_tesouro():
    """Obter dados do Tesouro Direto"""
    try:
        db = get_db()
        controller = MarketController(db)
        user_id = str(g.user["_id"])
        return controller.get_tesouro_direto(user_id)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@market_bp.route('/b3-indices', methods=['GET'])
@token_required
def get_indices():
    """Obter índices da B3"""
    try:
        db = get_db()
        controller = MarketController(db)
        user_id = str(g.user["_id"])
        return controller.get_b3_indices(user_id)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@market_bp.route('/api-calls', methods=['GET'])
@token_required
def get_api_history():
    """Histórico de chamadas de API"""
    try:
        db = get_db()
        controller = MarketController(db)
        user_id = str(g.user["_id"])
        limit = request.args.get('limit', 50, type=int)
        return controller.get_api_calls_history(user_id, limit)
    except Exception as e:
        return jsonify({"error": str(e)}), 500