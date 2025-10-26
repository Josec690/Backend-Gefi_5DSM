from datetime import datetime
from bson import ObjectId
from config.database import get_entradas_collection

class EntradaModel:
    
    @staticmethod
    def criar(usuario_id, descricao, valor, categoria, data):
        """Cria uma nova entrada"""
        entradas = get_entradas_collection()
        
        nova_entrada = {
            'usuario_id': usuario_id,
            'descricao': descricao,
            'valor': float(valor),
            'categoria': categoria,
            'data': data,
            'criado_em': datetime.utcnow()
        }
        
        resultado = entradas.insert_one(nova_entrada)
        return resultado.inserted_id
    
    @staticmethod
    def listar_por_usuario(usuario_id):
        """Lista todas as entradas de um usuário"""
        entradas = get_entradas_collection()
        return list(entradas.find({'usuario_id': usuario_id}).sort('data', -1))
    
    @staticmethod
    def buscar_por_id(entrada_id, usuario_id):
        """Busca uma entrada específica do usuário"""
        entradas = get_entradas_collection()
        return entradas.find_one({
            '_id': ObjectId(entrada_id),
            'usuario_id': usuario_id
        })
    
    @staticmethod
    def atualizar(entrada_id, usuario_id, dados):
        """Atualiza uma entrada"""
        entradas = get_entradas_collection()
        
        entradas.update_one(
            {'_id': ObjectId(entrada_id), 'usuario_id': usuario_id},
            {'$set': dados}
        )
    
    @staticmethod
    def deletar(entrada_id, usuario_id):
        """Deleta uma entrada"""
        entradas = get_entradas_collection()
        
        resultado = entradas.delete_one({
            '_id': ObjectId(entrada_id),
            'usuario_id': usuario_id
        })
        
        return resultado.deleted_count > 0
    
    @staticmethod
    def buscar_por_periodo(usuario_id, data_inicio, data_fim):
        """Busca entradas por período"""
        entradas = get_entradas_collection()
        
        return list(entradas.find({
            'usuario_id': usuario_id,
            'data': {'$gte': data_inicio, '$lt': data_fim}
        }))