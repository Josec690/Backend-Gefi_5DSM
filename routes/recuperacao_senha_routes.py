from flask import Blueprint
from controllers.recuperacao_senha_controller import RecuperacaoSenhaController

recuperacao_bp = Blueprint('recuperacao', __name__)

@recuperacao_bp.route('/recuperar-senha/solicitar', methods=['POST'])
def solicitar_codigo():
    """Solicita código de recuperação de senha"""
    return RecuperacaoSenhaController.solicitar_codigo()

@recuperacao_bp.route('/recuperar-senha/redefinir', methods=['POST'])
def redefinir_senha():
    """Redefine a senha usando o código"""
    return RecuperacaoSenhaController.redefinir_senha()
