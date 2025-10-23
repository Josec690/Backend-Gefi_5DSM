from datetime import datetime, timedelta
from flask import jsonify
from app.models.user_model import UserCreate, UserLogin, PasswordReset, PasswordChange
from app.utils.security import get_password_hash, verify_password, create_access_token, generate_reset_token
from app.utils.validators import validate_cpf
from app.config import Config
from bson import ObjectId

class AuthController:
    """Controller para operações de autenticação"""
    
    def __init__(self, db):
        self.db = db
    
    def register_user(self, user_data: dict):
        """Registra novo usuário"""
        try:
            user = UserCreate(**user_data)
            
            # Validar CPF
            if not validate_cpf(user.cpf_user):
                return {"error": "CPF inválido"}, 400
            
            # Verificar se usuário já existe
            existing = self.db.usuarios.find_one({
                "$or": [
                    {"email": user.email},
                    {"cpf_user": user.cpf_user}
                ]
            })
            
            if existing:
                return {"error": "Email ou CPF já cadastrado"}, 400
            
            # Criar usuário
            hashed_password = get_password_hash(user.password)
            user_dict = {
                "cpf_user": user.cpf_user,
                "full_name": user.full_name,
                "email": user.email,
                "password_hash": hashed_password,
                "registration_data": datetime.utcnow(),
                "password_updated_at": datetime.utcnow()
            }
            
            result = self.db.usuarios.insert_one(user_dict)
            user_dict["_id"] = str(result.inserted_id)
            
            return {
                "id": str(result.inserted_id),
                "email": user.email,
                "full_name": user.full_name,
                "message": "Usuário cadastrado com sucesso"
            }, 201
        
        except Exception as e:
            return {"error": str(e)}, 500
    
    def login_user(self, credentials: dict):
        """Realiza login do usuário"""
        try:
            user_login = UserLogin(**credentials)
            
            # Buscar usuário
            user = self.db.usuarios.find_one({"email": user_login.email})
            
            if not user or not verify_password(user_login.password, user["password_hash"]):
                return {"error": "Email ou senha incorretos"}, 401
            
            # Criar token
            access_token_expires = timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(
                data={"sub": user["email"]},
                expires_delta=access_token_expires
            )
            
            return {
                "access_token": access_token,
                "token_type": "bearer",
                "message": "Login realizado com sucesso"
            }, 200
        
        except Exception as e:
            return {"error": str(e)}, 500
    
    def change_password(self, user_id: str, password_data: dict):
        """Altera senha do usuário"""
        try:
            user = self.db.usuarios.find_one({"_id": ObjectId(user_id)})
            
            if not user:
                return {"error": "Usuário não encontrado"}, 404
            
            pwd_change = PasswordChange(**password_data)
            
            # Verificar senha atual
            if not verify_password(pwd_change.current_password, user["password_hash"]):
                return {"error": "Senha atual incorreta"}, 400
            
            # Atualizar senha
            hashed_password = get_password_hash(pwd_change.new_password)
            self.db.usuarios.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": {
                    "password_hash": hashed_password,
                    "password_updated_at": datetime.utcnow()
                }}
            )
            
            return {"message": "Senha alterada com sucesso"}, 200
        
        except Exception as e:
            return {"error": str(e)}, 500
    
    def request_password_reset(self, email: str):
        """Solicita reset de senha"""
        try:
            user = self.db.usuarios.find_one({"email": email})
            
            if not user:
                return {"message": "Se o email existir, você receberá instruções"}, 200
            
            reset_token = generate_reset_token()
            expires_at = datetime.utcnow() + timedelta(minutes=10)
            
            self.db.usuarios.update_one(
                {"email": email},
                {"$set": {
                    "reset_token": reset_token,
                    "reset_token_expires": expires_at
                }}
            )
            
            return {"message": "Email de recuperação enviado"}, 200
        
        except Exception as e:
            return {"error": str(e)}, 500