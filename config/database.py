from pymongo import MongoClient
import os

# Configurações do MongoDB
MONGODB_URL = "mongodb+srv://gefinanca_db:2spcZYs1YuCnfaGe@cluster0.e6fdms9.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
DATABASE_NAME = "gefinanca_db"

# Variáveis globais para o banco
client = None
db = None
usuarios_collection = None
entradas_collection = None
saidas_collection = None

def init_db():
    """Inicializa a conexão com o MongoDB"""
    global client, db, usuarios_collection, entradas_collection, saidas_collection
    
    try:
        client = MongoClient(MONGODB_URL)
        db = client[DATABASE_NAME]
        
        # Collections
        usuarios_collection = db['usuario']
        entradas_collection = db['entrada']
        saidas_collection = db['saida']
        
        # Testar conexão
        client.server_info()
        print("✅ Conectado ao MongoDB Atlas com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro ao conectar ao MongoDB: {e}")
        raise

def get_db():
    """Retorna a instância do banco de dados"""
    return db

def get_usuarios_collection():
    """Retorna a collection de usuários"""
    return usuarios_collection

def get_entradas_collection():
    """Retorna a collection de entradas"""
    return entradas_collection

def get_saidas_collection():
    """Retorna a collection de saídas"""
    return saidas_collection