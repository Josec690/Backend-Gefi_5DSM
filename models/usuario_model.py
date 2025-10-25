from datetime import datetime
from bson import ObjectId
from config.database import get_usuarios_collection
import bcrypt

class UsuarioModel:
    
    @staticmethod
    def criar(nome, email, cpf, senha):
        """Cria um novo usuário"""
        usuarios = get_usuarios_collection()
        
        novo_usuario = {
            'nome': nome,
            'email': email.lower(),
            'cpf': cpf,
            'senha': bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()),
            'respostas_questionario': {},
            'data_criacao': datetime.utcnow()
        }
        
        resultado = usuarios.insert_one(novo_usuario)
        return resultado.inserted_id
    
    @staticmethod
    def buscar_por_email(email):
        """Busca usuário por email"""
        usuarios = get_usuarios_collection()
        return usuarios.find_one({'email': email.lower()})
    
    @staticmethod
    def buscar_por_id(usuario_id):
        """Busca usuário por ID"""
        usuarios = get_usuarios_collection()
        return usuarios.find_one({'_id': ObjectId(usuario_id)})
    
    @staticmethod
    def buscar_por_cpf(cpf):
        """Busca usuário por CPF"""
        usuarios = get_usuarios_collection()
        return usuarios.find_one({'cpf': cpf})
    
    @staticmethod
    def atualizar_senha(usuario_id, nova_senha):
        """Atualiza a senha do usuário"""
        usuarios = get_usuarios_collection()
        senha_hash = bcrypt.hashpw(nova_senha.encode('utf-8'), bcrypt.gensalt())
        
        usuarios.update_one(
            {'_id': ObjectId(usuario_id)},
            {'$set': {'senha': senha_hash}}
        )
    
    @staticmethod
    def salvar_questionario(usuario_id, respostas):
        """Salva as respostas do questionário"""
        usuarios = get_usuarios_collection()
        
        usuarios.update_one(
            {'_id': ObjectId(usuario_id)},
            {'$set': {'respostas_questionario': respostas}}
        )
    
    @staticmethod
    def verificar_senha(senha, senha_hash):
        """Verifica se a senha está correta"""
        return bcrypt.checkpw(senha.encode('utf-8'), senha_hash)