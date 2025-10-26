from flask import request, jsonify
from models.entrada_model import EntradaModel
from datetime import datetime

class EntradaController:
    
    @staticmethod
    def criar(usuario_id):
        """Cria uma nova entrada financeira"""
        try:
            dados = request.get_json()
            
            descricao = dados.get('descricao', '').strip()
            valor = dados.get('valor', 0)
            categoria = dados.get('categoria', 'Outros').strip()
            data = dados.get('data', datetime.utcnow().isoformat())
            
            if not descricao:
                return jsonify({'erro': 'Descrição é obrigatória'}), 400
            
            if valor <= 0:
                return jsonify({'erro': 'Valor deve ser maior que zero'}), 400
            
            # Converter data
            data_obj = datetime.fromisoformat(data.replace('Z', '+00:00'))
            
            entrada_id = EntradaModel.criar(usuario_id, descricao, valor, categoria, data_obj)
            
            return jsonify({
                'mensagem': 'Entrada criada com sucesso',
                'id': str(entrada_id)
            }), 201
            
        except Exception as e:
            return jsonify({'erro': f'Erro ao criar entrada: {str(e)}'}), 500
    
    @staticmethod
    def listar(usuario_id):
        """Lista todas as entradas do usuário"""
        try:
            entradas = EntradaModel.listar_por_usuario(usuario_id)
            
            entradas_formatadas = []
            for entrada in entradas:
                entradas_formatadas.append({
                    'id': str(entrada['_id']),
                    'descricao': entrada['descricao'],
                    'valor': entrada['valor'],
                    'categoria': entrada['categoria'],
                    'data': entrada['data'].isoformat()
                })
            
            return jsonify(entradas_formatadas), 200
            
        except Exception as e:
            return jsonify({'erro': f'Erro ao listar entradas: {str(e)}'}), 500
    
    @staticmethod
    def atualizar(usuario_id, entrada_id):
        """Atualiza uma entrada existente"""
        try:
            dados = request.get_json()
            
            entrada = EntradaModel.buscar_por_id(entrada_id, usuario_id)
            
            if not entrada:
                return jsonify({'erro': 'Entrada não encontrada'}), 404
            
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
            
            EntradaModel.atualizar(entrada_id, usuario_id, atualizacao)
            
            return jsonify({'mensagem': 'Entrada atualizada com sucesso'}), 200
            
        except Exception as e:
            return jsonify({'erro': f'Erro ao atualizar entrada: {str(e)}'}), 500
    
    @staticmethod
    def deletar(usuario_id, entrada_id):
        """Deleta uma entrada"""
        try:
            sucesso = EntradaModel.deletar(entrada_id, usuario_id)
            
            if not sucesso:
                return jsonify({'erro': 'Entrada não encontrada'}), 404
            
            return jsonify({'mensagem': 'Entrada deletada com sucesso'}), 200
            
        except Exception as e:
            return jsonify({'erro': f'Erro ao deletar entrada: {str(e)}'}), 500