from flask import request, jsonify
from models.saida_model import SaidaModel
from datetime import datetime

class SaidaController:
    
    @staticmethod
    def criar(usuario_id):
        """Cria uma nova saída financeira"""
        try:
            dados = request.get_json()
            
            descricao = dados.get('descricao', '').strip()
            valor = dados.get('valor', 0)
            categoria = dados.get('categoria', 'Outros').strip()
            data = dados.get('data', datetime.utcnow().isoformat())
            eh_recorrente = dados.get('eh_recorrente', False)
            data_primeira_recorrencia = dados.get('data_primeira_recorrencia')
            
            if not descricao:
                return jsonify({'erro': 'Descrição é obrigatória'}), 400
            
            if valor <= 0:
                return jsonify({'erro': 'Valor deve ser maior que zero'}), 400
            
            # Converter data
            data_obj = datetime.fromisoformat(data.replace('Z', '+00:00'))
            
            saida_id = SaidaModel.criar(usuario_id, descricao, valor, categoria, data_obj, eh_recorrente)
            
            return jsonify({
                'mensagem': 'Saída criada com sucesso',
                'id': str(saida_id)
            }), 201
            
        except Exception as e:
            return jsonify({'erro': f'Erro ao criar saída: {str(e)}'}), 500
    
    @staticmethod
    def listar(usuario_id):
        """Lista todas as saídas do usuário"""
        try:
            saidas = SaidaModel.listar_por_usuario(usuario_id)
            
            saidas_formatadas = []
            for saida in saidas:
                saidas_formatadas.append({
                    'id': str(saida['_id']),
                    'descricao': saida['descricao'],
                    'valor': saida['valor'],
                    'categoria': saida['categoria'],
                    'data': saida['data'].isoformat(),
                    'eh_recorrente': saida.get('eh_recorrente', False)
                })
            
            return jsonify(saidas_formatadas), 200
            
        except Exception as e:
            return jsonify({'erro': f'Erro ao listar saídas: {str(e)}'}), 500
    
    @staticmethod
    def atualizar(usuario_id, saida_id):
        """Atualiza uma saída existente"""
        try:
            dados = request.get_json()
            
            saida = SaidaModel.buscar_por_id(saida_id, usuario_id)
            
            if not saida:
                return jsonify({'erro': 'Saída não encontrada'}), 404
            
            atualizacao = {}
            if 'descricao' in dados:
                atualizacao['descricao'] = dados['descricao'].strip()
            if 'valor' in dados:
                if dados['valor'] <= 0:
                    return jsonify({'erro': 'Valor deve ser maior que zero'}), 400
                atualizacao['valor'] = float(dados['valor'])
            if 'categoria' in dados:
                atualizacao['categoria'] = dados['categoria'].strip()
            if 'data' in dados:
                atualizacao['data'] = datetime.fromisoformat(dados['data'].replace('Z', '+00:00'))
            if 'eh_recorrente' in dados:
                atualizacao['eh_recorrente'] = dados['eh_recorrente']
            
            SaidaModel.atualizar(saida_id, usuario_id, atualizacao)
            
            return jsonify({'mensagem': 'Saída atualizada com sucesso'}), 200
            
        except Exception as e:
            return jsonify({'erro': f'Erro ao atualizar saída: {str(e)}'}), 500
    
    @staticmethod
    def deletar(usuario_id, saida_id):
        """Deleta uma saída"""
        try:
            sucesso = SaidaModel.deletar(saida_id, usuario_id)
            
            if not sucesso:
                return jsonify({'erro': 'Saída não encontrada'}), 404
            
            return jsonify({'mensagem': 'Saída deletada com sucesso'}), 200
            
        except Exception as e:
            return jsonify({'erro': f'Erro ao deletar saída: {str(e)}'}), 500