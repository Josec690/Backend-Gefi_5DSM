from flask import request, jsonify, g
from functools import wraps
from app.utils.security import verify_token
from app.database.connection import get_db
from bson import ObjectId

def token_required(f):
    """Decorator para verificar JWT"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Verificar header Authorization
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({"message": "Token inválido"}), 401
        
        if not token:
            return jsonify({"message": "Token ausente"}), 401
        
        # Verificar token
        token_data = verify_token(token)
        if not token_data:
            return jsonify({"message": "Token inválido ou expirado"}), 401
        
        # Buscar usuário no banco
        db = get_db()
        user = db.usuarios.find_one({"email": token_data["email"]})
        if not user:
            return jsonify({"message": "Usuário não encontrado"}), 401
        
        # Armazenar usuário no contexto da requisição
        g.user = user
        return f(*args, **kwargs)
    
    return decorated