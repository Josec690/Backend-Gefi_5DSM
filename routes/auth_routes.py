from flask import Blueprint
from controllers.auth_controller import AuthController
from utils.auth import token_obrigatorio

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/cadastro', methods=['POST'])
def cadastro():
    return AuthController.cadastro()

@auth_bp.route('/login', methods=['POST'])
def login():
    return AuthController.login()

@auth_bp.route('/recuperar-senha', methods=['POST'])
def recuperar_senha():
    return AuthController.recuperar_senha()

@auth_bp.route('/mudar-senha', methods=['PUT'])
@token_obrigatorio
def mudar_senha(usuario_id):
    return AuthController.mudar_senha(usuario_id)