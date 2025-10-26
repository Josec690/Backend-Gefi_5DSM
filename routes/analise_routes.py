from flask import Blueprint
from controllers.analise_controller import AnaliseController
from utils.auth import token_obrigatorio

analise_bp = Blueprint('analise', __name__)

@analise_bp.route('/balanco', methods=['GET'])
@token_obrigatorio
def calcular_balanco(usuario_id):
    return AnaliseController.calcular_balanco(usuario_id)

@analise_bp.route('/proximas-saidas', methods=['GET'])
@token_obrigatorio
def proximas_saidas(usuario_id):
    return AnaliseController.proximas_saidas(usuario_id)

@analise_bp.route('/categorias-gastos', methods=['GET'])
@token_obrigatorio
def categorias_gastos(usuario_id):
    return AnaliseController.categorias_gastos(usuario_id)