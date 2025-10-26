from flask import Blueprint
from controllers.user_controller import UserController
from utils.auth import token_obrigatorio

user_bp = Blueprint('user', __name__)

@user_bp.route('/usuario', methods=['GET'])
@token_obrigatorio
def get_usuario(usuario_id):
    return UserController.get_usuario(usuario_id)

@user_bp.route('/questionario', methods=['POST'])
@token_obrigatorio
def salvar_questionario(usuario_id):
    return UserController.salvar_questionario(usuario_id)