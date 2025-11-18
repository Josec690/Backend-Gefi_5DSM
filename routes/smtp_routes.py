from flask import Blueprint, request, jsonify
from utils.email_sender import send_email
import os

smtp_bp = Blueprint('smtp', __name__)


@smtp_bp.route('/smtp/test', methods=['POST'])
def smtp_test():
    """Envia um e-mail de teste usando as credenciais SMTP configuradas.

    Body opcional (JSON):
      - to: destinatário (default = SMTP_USER)
      - subject: assunto
      - text: corpo texto
      - html: corpo HTML
    """
    data = request.get_json(silent=True) or {}
    to_email = data.get('to') or os.getenv('SMTP_USER')
    subject = data.get('subject') or 'Teste SMTP - GeFi'
    text_body = data.get('text') or 'Teste de envio SMTP (texto).'
    html_body = data.get('html') or (
        "<div style='font-family:Arial,sans-serif'>"
        "<h3>Teste SMTP - GeFi</h3>"
        "<p>Se você recebeu este e-mail, o SMTP está configurado corretamente.</p>"
        "</div>"
    )

    if not to_email:
        return jsonify({'ok': False, 'erro': 'Defina o destinatário no body (to) ou a variável SMTP_USER'}), 400

    ok, erro = send_email(to_email, subject, html_body, text_body)
    if ok:
        return jsonify({'ok': True, 'mensagem': 'E-mail enviado', 'to': to_email}), 200
    return jsonify({'ok': False, 'erro': erro}), 500
