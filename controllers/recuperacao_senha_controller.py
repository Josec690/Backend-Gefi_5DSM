from flask import jsonify, request
from models.usuario_model import UsuarioModel
from config.database import get_usuarios_collection
from utils.email_sender import send_email
import random
import string
from datetime import datetime, timedelta
import os
import bcrypt

# Armazenamento temporário de códigos (em produção, use Redis ou banco)
_codigos_recuperacao = {}

class RecuperacaoSenhaController:
    
    @staticmethod
    def gerar_codigo():
        """Gera um código de 6 dígitos"""
        return ''.join(random.choices(string.digits, k=6))
    
    @staticmethod
    def solicitar_codigo():
        """Envia código de recuperação para o e-mail"""
        try:
            data = request.get_json()
            email = data.get('email', '').strip().lower()
            
            if not email:
                return jsonify({'erro': 'E-mail é obrigatório'}), 400
            
            # Verificar se usuário existe
            usuario = UsuarioModel.buscar_por_email(email)
            if not usuario:
                return jsonify({'erro': 'E-mail não encontrado'}), 404
            
            # Gerar código
            codigo = RecuperacaoSenhaController.gerar_codigo()
            
            # Armazenar código com validade de 15 minutos
            _codigos_recuperacao[email] = {
                'codigo': codigo,
                'expira_em': datetime.utcnow() + timedelta(minutes=15),
                'tentativas': 0
            }
            
            # Enviar e-mail real
            assunto = "Código de recuperação - GeFi"
            texto = (
                f"Seu código de recuperação é: {codigo}.\n"
                "Ele expira em 15 minutos.\n\n"
                "Se você não solicitou, ignore este e-mail."
            )
            html = f"""
                <div style='font-family:Arial,sans-serif;font-size:16px;color:#222'>
                  <h2>GeFi - Recuperação de Senha</h2>
                  <p>Olá,</p>
                  <p>Use o código abaixo para redefinir sua senha. Ele expira em <b>15 minutos</b>:</p>
                  <div style='font-size:28px;font-weight:700;letter-spacing:3px;margin:16px 0;padding:12px 16px;background:#f4f4f4;border-radius:8px;display:inline-block;'>
                    {codigo}
                  </div>
                  <p>Se você não solicitou essa recuperação, ignore este e-mail.</p>
                  <hr/>
                  <p style='font-size:12px;color:#666'>Mensagem automática • Não responda</p>
                </div>
            """

            ok, erro = send_email(email, assunto, html, texto)
            if not ok:
                # Não exponha detalhes sensíveis ao cliente em prod
                print(f"❌ Falha ao enviar e-mail para {email}: {erro}")
                return jsonify({'erro': 'Não foi possível enviar o e-mail de recuperação. Verifique as configurações SMTP.'}), 500
            
            # Em desenvolvimento, opcionalmente retornar o código para facilitar testes
            debug_return = os.getenv('RECOVERY_DEBUG_RETURN_CODE', 'false').lower() in ('1','true','yes','on')
            payload = { 'mensagem': 'Código de recuperação enviado para o e-mail' }
            if debug_return:
                payload['codigo_debug'] = codigo
            return jsonify(payload), 200
            
        except Exception as e:
            print(f"Erro ao solicitar código: {e}")
            return jsonify({'erro': 'Erro ao processar solicitação'}), 500
    
    @staticmethod
    def redefinir_senha():
        """Redefine a senha usando o código de recuperação"""
        try:
            data = request.get_json()
            email = data.get('email', '').strip().lower()
            codigo = data.get('codigo', '').strip()
            nova_senha = data.get('nova_senha', '').strip()
            
            # Validações
            if not email or not codigo or not nova_senha:
                return jsonify({'erro': 'Todos os campos são obrigatórios'}), 400
            
            if len(nova_senha) < 6:
                return jsonify({'erro': 'A senha deve ter no mínimo 6 caracteres'}), 400
            
            # Verificar se existe código para este e-mail
            info_codigo = _codigos_recuperacao.get(email)
            if not info_codigo:
                return jsonify({'erro': 'Código inválido ou expirado'}), 400
            
            # Verificar se código expirou
            if datetime.utcnow() > info_codigo['expira_em']:
                del _codigos_recuperacao[email]
                return jsonify({'erro': 'Código expirado. Solicite um novo código'}), 400
            
            # Verificar tentativas (máximo 3)
            if info_codigo['tentativas'] >= 3:
                del _codigos_recuperacao[email]
                return jsonify({'erro': 'Número máximo de tentativas excedido. Solicite um novo código'}), 400
            
            # Verificar se o código está correto
            if info_codigo['codigo'] != codigo:
                info_codigo['tentativas'] += 1
                tentativas_restantes = 3 - info_codigo['tentativas']
                return jsonify({
                    'erro': f'Código incorreto. {tentativas_restantes} tentativa(s) restante(s)'
                }), 400
            
            # Atualizar senha do usuário
            usuarios_collection = get_usuarios_collection()
            senha_hash = bcrypt.hashpw(nova_senha.encode('utf-8'), bcrypt.gensalt())
            resultado = usuarios_collection.update_one(
                {'email': email},
                {'$set': {'senha': senha_hash}}
            )
            
            if resultado.modified_count == 0:
                return jsonify({'erro': 'Erro ao atualizar senha'}), 500
            
            # Remover código usado
            del _codigos_recuperacao[email]
            
            print(f"✅ Senha redefinida com sucesso para {email}")
            
            return jsonify({'mensagem': 'Senha redefinida com sucesso'}), 200
            
        except Exception as e:
            print(f"Erro ao redefinir senha: {e}")
            return jsonify({'erro': 'Erro ao processar solicitação'}), 500
    
    @staticmethod
    def limpar_codigos_expirados():
        """Remove códigos expirados (executar periodicamente)"""
        agora = datetime.utcnow()
        emails_expirados = [
            email for email, info in _codigos_recuperacao.items()
            if agora > info['expira_em']
        ]
        for email in emails_expirados:
            del _codigos_recuperacao[email]
        
        if emails_expirados:
            print(f"🧹 Removidos {len(emails_expirados)} códigos expirados")
