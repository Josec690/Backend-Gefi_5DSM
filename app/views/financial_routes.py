from flask import Blueprint, request, jsonify
from app.controllers.financial_controller import FinancialController
from app.database.connection import get_db
from app.middlewares.auth_middleware import token_required
from flask import g
from bson import ObjectId

financial_bp = Blueprint('financial', __name__, url_prefix='/financial')

@financial_bp.route('/entrada', methods=['POST'])
@token_required
def create_entrada():
    """Criar nova entrada financeira"""
    try:
        db = get_db()
        controller = FinancialController(db)
        user_id = str(g.user["_id"])
        return controller.create_entrada(user_id, request.get_json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@financial_bp.route('/entradas', methods=['GET'])
@token_required
def get_entradas():
    """Listar entradas do usuário"""
    try:
        db = get_db()
        controller = FinancialController(db)
        user_id = str(g.user["_id"])
        skip = request.args.get('skip', 0, type=int)
        limit = request.args.get('limit', 100, type=int)
        return controller.get_entradas(user_id, skip, limit)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@financial_bp.route('/saida', methods=['POST'])
@token_required
def create_saida():
    """Criar nova saída financeira"""
    try:
        db = get_db()
        controller = FinancialController(db)
        user_id = str(g.user["_id"])
        return controller.create_saida(user_id, request.get_json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@financial_bp.route('/resumo', methods=['GET'])
@token_required
def get_resumo():
    """Resumo financeiro do usuário"""
    try:
        db = get_db()
        controller = FinancialController(db)
        user_id = str(g.user["_id"])
        mes = request.args.get('mes', None, type=int)
        ano = request.args.get('ano', None, type=int)
        return controller.get_resumo_financeiro(user_id, mes, ano)
    except Exception as e:
        return jsonify({"error": str(e)}), 500