from flask import Blueprint
from controllers.investimento_controller import InvestimentoController
from utils.auth import token_obrigatorio

investimento_bp = Blueprint('investimento', __name__)

@investimento_bp.route('/investimentos', methods=['GET'])
@token_obrigatorio
def listar_investimentos(usuario_id):
    return InvestimentoController.listar()