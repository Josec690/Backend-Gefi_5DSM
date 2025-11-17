from flask import Blueprint
from controllers.investimento_controller import InvestimentoController
from utils.auth import token_obrigatorio

investimento_bp = Blueprint("investimento", __name__)


@investimento_bp.route("/investimentos", methods=["GET"])
@token_obrigatorio
def listar_investimentos(usuario_id):
    return InvestimentoController.listar()


@investimento_bp.route("/investimentos/cotacao", methods=["GET"])
def buscar_cotacao():
    """Busca cotação de um ou mais tickers (pública para facilitar testes)"""
    return InvestimentoController.cotacao()


@investimento_bp.route("/investimentos/em-alta", methods=["GET"])
def investimentos_em_alta():
    """Retorna investimentos com maior valorização do dia (pública)"""
    return InvestimentoController.em_alta()


@investimento_bp.route("/investimentos/tesouro", methods=["GET"])
def listar_tesouro():
    """Lista títulos do Tesouro Direto disponíveis (pública)"""
    return InvestimentoController.listar_tesouro()
