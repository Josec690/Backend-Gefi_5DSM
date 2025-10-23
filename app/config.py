import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configurações gerais da aplicação"""
    MONGODB_URL = os.getenv("MONGODB_URL")
    DATABASE_NAME = os.getenv("DATABASE_NAME")
    SECRET_KEY = os.getenv("SECRET_KEY")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    CRYPTO_KEY = os.getenv("CRYPTO_KEY")
    FLASK_ENV = os.getenv("FLASK_ENV", "production")
    JSON_SORT_KEYS = False

class DevelopmentConfig(Config):
    """Configurações para desenvolvimento"""
    DEBUG = True

class ProductionConfig(Config):
    """Configurações para produção"""
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}