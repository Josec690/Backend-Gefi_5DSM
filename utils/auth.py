import jwt
from datetime import datetime, timedelta
from flask import request, jsonify
from functools import wraps
from bson import ObjectId
from models.usuario_model import UsuarioModel
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
JWT_ALGORITHM = os.getenv('JWT_ALGORITHM')

def gerar_token(usuario_id):
    """Gera token JWT"""
    payload = {
        'usuario_id': str(usuario_id),
        'exp': datetime.utcnow() + timedelta(days=7)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=JWT_ALGORITHM)

def token_obrigatorio(f):
    """Decorator para rotas que exigem autenticação"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'erro': 'Token não fornecido'}), 401
        
        try:
            # Remove 'Bearer ' do token se existir
            if token.startswith('Bearer '):
                token = token[7:]
            
            dados = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
            usuario_id = dados['usuario_id']
            
            # Verifica se usuário existe
            usuario = UsuarioModel.buscar_por_id(usuario_id)
            if not usuario:
                return jsonify({'erro': 'Usuário não encontrado'}), 401
            
            # Passa o usuario_id para a função
            return f(usuario_id, *args, **kwargs)
            
        except jwt.ExpiredSignatureError:
            return jsonify({'erro': 'Token expirado'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'erro': 'Token inválido'}), 401
        except Exception as e:
            return jsonify({'erro': f'Erro na autenticação: {str(e)}'}), 401
    
    return decorated