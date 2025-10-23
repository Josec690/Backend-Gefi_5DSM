import re

def validate_cpf(cpf: str) -> bool:
    """Valida CPF"""
    cpf = re.sub(r'[^0-9]', '', cpf)
    
    if len(cpf) != 11:
        return False
    
    if cpf == cpf[0] * 11:
        return False
    
    sum_digits = sum(int(cpf[i]) * (10 - i) for i in range(9))
    digit1 = (sum_digits * 10 % 11) % 10
    
    if digit1 != int(cpf[9]):
        return False
    
    sum_digits = sum(int(cpf[i]) * (11 - i) for i in range(10))
    digit2 = (sum_digits * 10 % 11) % 10
    
    return digit2 == int(cpf[10])

def validate_password_strength(password: str) -> tuple:
    """Valida força da senha"""
    if len(password) < 8:
        return False, "Senha deve ter no mínimo 8 caracteres"
    
    if len(password) > 100:
        return False, "Senha muito longa"
    
    if not re.search(r'[A-Z]', password):
        return False, "Senha deve ter letra maiúscula"
    
    if not re.search(r'[a-z]', password):
        return False, "Senha deve ter letra minúscula"
    
    if not re.search(r'\d', password):
        return False, "Senha deve ter número"
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Senha deve ter caractere especial"
    
    return True, "Senha válida"