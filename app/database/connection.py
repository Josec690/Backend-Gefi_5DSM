from pymongo import MongoClient
from app.config import Config

class Database:
    client = None
    db = None

def init_db():
    """Inicializa conexão com MongoDB"""
    try:
        Database.client = MongoClient(Config.MONGODB_URL)
        Database.db = Database.client[Config.DATABASE_NAME]
        print("✅ Conectado ao MongoDB Atlas")
    except Exception as e:
        print(f"❌ Erro ao conectar ao MongoDB: {e}")
        raise

def close_db():
    """Fecha conexão com MongoDB"""
    if Database.client:
        Database.client.close()
        print("❌ Desconectado do MongoDB")

def get_db():
    """Retorna instância do banco de dados"""
    return Database.db