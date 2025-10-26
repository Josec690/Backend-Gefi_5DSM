from flask import Blueprint
from controllers.saida_controller import SaidaController
from utils.auth import token_obrigatorio

saida_bp = Blueprint('saida', __name__)

@saida_bp.route('/saida', methods=['POST'])
@token_obrigatorio
def criar_saida(usuario_id):
    return SaidaController.criar(usuario_id)

@saida_bp.route('/saidas', methods=['GET'])
@token_obrigatorio
def listar_saidas(usuario_id):
    return SaidaController.listar(usuario_id)

@saida_bp.route('/saida/<saida_id>', methods=['PUT'])
@token_obrigatorio
def atualizar_saida(usuario_id, saida_id):
    return SaidaController.atualizar(usuario_id, saida_id)

@saida_bp.route('/saida/<saida_id>', methods=['DELETE'])
@token_obrigatorio
def deletar_saida(usuario_id, saida_id):
    return SaidaController.deletar(usuario_id, saida_id)