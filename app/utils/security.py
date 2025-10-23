from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
import secrets
import base64
from cryptography.fernet import Fernet
from app.config import Config
from typing import Optional

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

cipher_suite = Fernet(
    Config.CRYPTO_KEY.encode() 
    if len(Config.CRYPTO_KEY.encode()) == 44 
    else base64.urlsafe_b64encode(Config.CRYPTO_KEY.encode()[:32])
)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha está correta"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Gera hash da senha"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Cria token JWT"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, 
        Config.SECRET_KEY, 
        algorithm=Config.JWT_ALGORITHM
    )
    return encoded_jwt

def verify_token(token: str) -> Optional[dict]:
    """Verifica e decodifica token JWT"""
    try:
        payload = jwt.decode(
            token, 
            Config.SECRET_KEY, 
            algorithms=[Config.JWT_ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            return None
        return {"email": email}
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def encrypt_sensitive_data(data: str) -> str:
    """Criptografa dados sensíveis"""
    return cipher_suite.encrypt(data.encode()).decode()

def decrypt_sensitive_data(encrypted_data: str) -> str:
    """Descriptografa dados sensíveis"""
    return cipher_suite.decrypt(encrypted_data.encode()).decode()

def generate_reset_token() -> str:
    """Gera token para reset de senha"""
    return secrets.token_urlsafe(32)