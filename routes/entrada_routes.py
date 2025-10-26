from flask import Blueprint
from controllers.entrada_controller import EntradaController
from utils.auth import token_obrigatorio

entrada_bp = Blueprint('entrada', __name__)

@entrada_bp.route('/entrada', methods=['POST'])
@token_obrigatorio
def criar_entrada(usuario_id):
    return EntradaController.criar(usuario_id)

@entrada_bp.route('/entradas', methods=['GET'])
@token_obrigatorio
def listar_entradas(usuario_id):
    return EntradaController.listar(usuario_id)

@entrada_bp.route('/entrada/<entrada_id>', methods=['PUT'])
@token_obrigatorio
def atualizar_entrada(usuario_id, entrada_id):
    return EntradaController.atualizar(usuario_id, entrada_id)

@entrada_bp.route('/entrada/<entrada_id>', methods=['DELETE'])
@token_obrigatorio
def deletar_entrada(usuario_id, entrada_id):
    return EntradaController.deletar(usuario_id, entrada_id)