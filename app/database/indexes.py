from pymongo import ASCENDING

def create_indexes(db):
    """Cria índices necessários nas coleções"""
    try:
        # Índices para usuários
        db.usuarios.create_index([("email", ASCENDING)], unique=True)
        db.usuarios.create_index([("cpf_user", ASCENDING)], unique=True)
        
        # Índices para entradas e saídas
        db.entradas.create_index([("user_id", ASCENDING)])
        db.entradas.create_index([("entry_data", ASCENDING)])
        
        db.saidas.create_index([("user_id", ASCENDING)])
        db.saidas.create_index([("out_data", ASCENDING)])
        
        # Índices para APIs
        db.apis.create_index([("user_id", ASCENDING)])
        
        print("✅ Índices criados com sucesso")
    except Exception as e:
        print(f"❌ Erro ao criar índices: {e}")