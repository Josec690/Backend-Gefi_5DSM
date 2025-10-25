import re

def validar_email(email):
    """Valida formato de email"""
    padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(padrao, email) is not None

def validar_cpf(cpf):
    """Validação básica de CPF (apenas formato)"""
    cpf_limpo = re.sub(r'\D', '', cpf)
    return len(cpf_limpo) == 11

def validar_senha(senha):
    """Valida se a senha tem no mínimo 6 caracteres"""
    return len(senha) >= 6