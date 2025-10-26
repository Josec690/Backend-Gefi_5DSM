from flask import request, jsonify
from models.usuario_model import UsuarioModel

class UserController:
    
    @staticmethod
    def get_usuario(usuario_id):
        """Busca dados do usuário autenticado"""
        try:
            usuario = UsuarioModel.buscar_por_id(usuario_id)
            
            if not usuario:
                return jsonify({'erro': 'Usuário não encontrado'}), 404
            
            return jsonify({
                'id': str(usuario['_id']),
                'nome': usuario['nome'],
                'email': usuario['email'],
                'cpf': usuario['cpf'],
                'respostas_questionario': usuario.get('respostas_questionario', {}),
                'data_criacao': usuario['data_criacao'].isoformat()
            }), 200
            
        except Exception as e:
            return jsonify({'erro': f'Erro ao buscar usuário: {str(e)}'}), 500
    
    @staticmethod
    def salvar_questionario(usuario_id):
        """Salva respostas do questionário inicial"""
        try:
            dados = request.get_json()
            respostas = dados.get('respostas', {})
            
            if not respostas:
                return jsonify({'erro': 'Respostas não fornecidas'}), 400
            
            UsuarioModel.salvar_questionario(usuario_id, respostas)
            
            return jsonify({'mensagem': 'Questionário salvo com sucesso'}), 200
            
        except Exception as e:
            return jsonify({'erro': f'Erro ao salvar questionário: {str(e)}'}), 500