from flask import request, jsonify, current_app
from models.usuario_model import UsuarioModel
from utils.validators import validar_email, validar_cpf, validar_senha
from utils.auth import gerar_token
from datetime import datetime

class AuthController:
    
    @staticmethod
    def cadastro():
        """Cadastro de novo usuário"""
        try:
            dados = request.get_json()
            
            # Extrair dados
            nome = dados.get('nome', '').strip()
            email = dados.get('email', '').strip().lower()
            cpf = dados.get('cpf', '').strip()
            senha = dados.get('senha', '')
            
            # Validações
            if not all([nome, email, cpf, senha]):
                return jsonify({'erro': 'Todos os campos são obrigatórios'}), 400
            
            if not validar_email(email):
                return jsonify({'erro': 'Email inválido'}), 400
            
            if not validar_cpf(cpf):
                return jsonify({'erro': 'CPF inválido'}), 400
            
            if not validar_senha(senha):
                return jsonify({'erro': 'Senha deve ter no mínimo 6 caracteres'}), 400
            
            # Verificar se já existe
            if UsuarioModel.buscar_por_email(email):
                return jsonify({'erro': 'Email já cadastrado'}), 409
            
            if UsuarioModel.buscar_por_cpf(cpf):
                return jsonify({'erro': 'CPF já cadastrado'}), 409
            
            # Criar usuário
            usuario_id = UsuarioModel.criar(nome, email, cpf, senha)
            token = gerar_token(usuario_id)
            
            return jsonify({
                'mensagem': 'Usuário cadastrado com sucesso',
                'token': token,
                'usuario_id': str(usuario_id)
            }), 201
            
        except Exception as e:
            return jsonify({'erro': f'Erro ao cadastrar: {str(e)}'}), 500
    
    @staticmethod
    def login():
        """Login de usuário"""
        try:
            dados = request.get_json()
            email = dados.get('email', '').strip().lower()
            senha = dados.get('senha', '')
            
            if not email or not senha:
                return jsonify({'erro': 'Email e senha são obrigatórios'}), 400
            
            # Buscar usuário
            usuario = UsuarioModel.buscar_por_email(email)
            
            if not usuario or not UsuarioModel.verificar_senha(senha, usuario['senha']):
                return jsonify({'erro': 'Email ou senha incorretos'}), 401
            
            token = gerar_token(usuario['_id'])
            
            return jsonify({
                'mensagem': 'Login realizado com sucesso',
                'token': token,
                'usuario': {
                    'id': str(usuario['_id']),
                    'nome': usuario['nome'],
                    'email': usuario['email'],
                    'cpf': usuario['cpf']
                }
            }), 200
            
        except Exception as e:
            return jsonify({'erro': f'Erro ao fazer login: {str(e)}'}), 500
    
    @staticmethod
    def recuperar_senha():
        """Solicita recuperação de senha"""
        try:
            dados = request.get_json()
            email = dados.get('email', '').strip().lower()
            
            if not email:
                return jsonify({'erro': 'Email é obrigatório'}), 400
            
            usuario = UsuarioModel.buscar_por_email(email)
            
            # Por segurança, sempre retorna sucesso
            if usuario:
                # TODO: Implementar envio de email real
                pass
            
            return jsonify({
                'mensagem': 'Se o email existir, um link de recuperação será enviado'
            }), 200
            
        except Exception as e:
            return jsonify({'erro': f'Erro ao recuperar senha: {str(e)}'}), 500
    
    @staticmethod
    def mudar_senha(usuario_id):
        """Muda a senha do usuário autenticado"""
        try:
            dados = request.get_json()
            senha_atual = dados.get('senha_atual', '')
            senha_nova = dados.get('senha_nova', '')
            
            if not senha_atual or not senha_nova:
                return jsonify({'erro': 'Senha atual e nova são obrigatórias'}), 400
            
            if not validar_senha(senha_nova):
                return jsonify({'erro': 'Nova senha deve ter no mínimo 6 caracteres'}), 400
            
            usuario = UsuarioModel.buscar_por_id(usuario_id)
            
            if not UsuarioModel.verificar_senha(senha_atual, usuario['senha']):
                return jsonify({'erro': 'Senha atual incorreta'}), 401
            
            # Atualizar senha
            UsuarioModel.atualizar_senha(usuario_id, senha_nova)
            
            return jsonify({'mensagem': 'Senha alterada com sucesso'}), 200
            
        except Exception as e:
            return jsonify({'erro': f'Erro ao mudar senha: {str(e)}'}), 500