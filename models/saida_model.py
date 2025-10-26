from datetime import datetime
from bson import ObjectId
from config.database import get_saidas_collection

class SaidaModel:
    
    @staticmethod
    def criar(usuario_id, descricao, valor, categoria, data, eh_recorrente=False):
        """Cria uma nova saída"""
        saidas = get_saidas_collection()
        
        nova_saida = {
            'usuario_id': usuario_id,
            'descricao': descricao,
            'valor': float(valor),
            'categoria': categoria,
            'data': data,
            'eh_recorrente': eh_recorrente,
            'criado_em': datetime.utcnow()
        }
        
        resultado = saidas.insert_one(nova_saida)
        return resultado.inserted_id
    
    @staticmethod
    def listar_por_usuario(usuario_id):
        """Lista todas as saídas de um usuário"""
        saidas = get_saidas_collection()
        return list(saidas.find({'usuario_id': usuario_id}).sort('data', -1))
    
    @staticmethod
    def buscar_por_id(saida_id, usuario_id):
        """Busca uma saída específica do usuário"""
        saidas = get_saidas_collection()
        return saidas.find_one({
            '_id': ObjectId(saida_id),
            'usuario_id': usuario_id
        })
    
    @staticmethod
    def atualizar(saida_id, usuario_id, dados):
        """Atualiza uma saída"""
        saidas = get_saidas_collection()
        
        saidas.update_one(
            {'_id': ObjectId(saida_id), 'usuario_id': usuario_id},
            {'$set': dados}
        )
    
    @staticmethod
    def deletar(saida_id, usuario_id):
        """Deleta uma saída"""
        saidas = get_saidas_collection()
        
        resultado = saidas.delete_one({
            '_id': ObjectId(saida_id),
            'usuario_id': usuario_id
        })
        
        return resultado.deleted_count > 0
    
    @staticmethod
    def buscar_por_periodo(usuario_id, data_inicio, data_fim):
        """Busca saídas por período"""
        saidas = get_saidas_collection()
        
        return list(saidas.find({
            'usuario_id': usuario_id,
            'data': {'$gte': data_inicio, '$lt': data_fim}
        }))
    
    @staticmethod
    def buscar_recorrentes_proximas(usuario_id, data_inicio, data_fim, limite=5):
        """Busca próximas saídas recorrentes"""
        saidas = get_saidas_collection()
        
        return list(saidas.find({
            'usuario_id': usuario_id,
            'eh_recorrente': True,
            'data': {'$gte': data_inicio, '$lt': data_fim}
        }).sort('data', 1).limit(limite))
    
    @staticmethod
    def agrupar_por_categoria(usuario_id, data_inicio, data_fim):
        """Agrupa saídas por categoria"""
        saidas = get_saidas_collection()
        
        pipeline = [
            {
                '$match': {
                    'usuario_id': usuario_id,
                    'data': {'$gte': data_inicio, '$lt': data_fim}
                }
            },
            {
                '$group': {
                    '_id': '$categoria',
                    'total': {'$sum': '$valor'},
                    'quantidade': {'$sum': 1}
                }
            },
            {
                '$sort': {'total': -1}
            }
        ]
        
        return list(saidas.aggregate(pipeline))