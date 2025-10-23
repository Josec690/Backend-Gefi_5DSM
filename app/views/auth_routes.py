from flask import Blueprint, request, jsonify
from app.controllers.auth_controller import AuthController
from app.database.connection import get_db
from app.middlewares.auth_middleware import token_required
from flask import g

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    """Cadastro de novo usuário"""
    try:
        db = get_db()
        controller = AuthController(db)
        return controller.register_user(request.get_json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login do usuário"""
    try:
        db = get_db()
        controller = AuthController(db)
        return controller.login_user(request.get_json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@auth_bp.route('/change-password', methods=['PUT'])
@token_required
def change_password():
    """Alterar senha (usuário logado)"""
    try:
        db = get_db()
        controller = AuthController(db)
        user_id = str(g.user["_id"])
        return controller.change_password(user_id, request.get_json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@auth_bp.route('/request-password-reset', methods=['POST'])
def request_reset():
    """Solicita reset de senha"""
    try:
        db = get_db()
        controller = AuthController(db)
        data = request.get_json()
        return controller.request_password_reset(data.get("email"))
    except Exception as e:
        return jsonify({"error": str(e)}), 500