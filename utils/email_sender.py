from email.message import EmailMessage
import smtplib
import ssl
import os
from dotenv import load_dotenv

"""
Melhorias:
- Usa cadeia de certificados do certifi (quando disponível) ou bundle customizado via env `SMTP_CA_BUNDLE`.
- Opção de desabilitar verificação em DEV via `SMTP_ALLOW_INVALID_CERTS` (false por padrão).
- Normaliza App Password do Gmail removendo espaços acidentais.
"""

load_dotenv()

def _build_ssl_context():
    """Constrói o contexto SSL com base nas variáveis de ambiente.

    - SMTP_ALLOW_INVALID_CERTS: se 'true', desabilita a verificação (apenas DEV)
    - SMTP_CA_BUNDLE: caminho para um CA bundle (.pem) customizado
    - Tenta usar certifi automaticamente se instalado
    """
    allow_invalid = os.getenv('SMTP_ALLOW_INVALID_CERTS', 'false').lower() in ('1', 'true', 'yes', 'on')
    ca_bundle = os.getenv('SMTP_CA_BUNDLE')

    if allow_invalid:
        # Atenção: apenas para desenvolvimento! Não use em produção.
        return ssl._create_unverified_context()

    cafile = None
    # Prioriza bundle customizado
    if ca_bundle and os.path.exists(ca_bundle):
        cafile = ca_bundle
    else:
        # Tenta usar certifi se disponível
        try:
            import certifi  # type: ignore
            cafile = certifi.where()
        except Exception:
            cafile = None

    # Cria contexto com ou sem cafile
    try:
        return ssl.create_default_context(cafile=cafile) if cafile else ssl.create_default_context()
    except Exception:
        # Fallback seguro
        return ssl.create_default_context()

def send_email(to_email: str, subject: str, html_body: str, text_body: str | None = None):
    """Envia e-mail via SMTP usando variáveis de ambiente.

    Variáveis necessárias:
      - SMTP_HOST
      - SMTP_PORT (ex: 587 TLS, 465 SSL)
      - SMTP_USER
      - SMTP_PASSWORD
      - SMTP_FROM (opcional; padrão = SMTP_USER)
      - SMTP_TLS (true/false) indica STARTTLS quando porta 25/587
    Retorna: (ok: bool, erro: str | None)
    """
    host = os.getenv('SMTP_HOST')
    port = int(os.getenv('SMTP_PORT', '587'))
    user = os.getenv('SMTP_USER')
    # Normaliza App Password do Gmail removendo espaços
    raw_password = os.getenv('SMTP_PASSWORD') or ''
    password = raw_password.replace(' ', '') if raw_password else raw_password
    from_email = os.getenv('SMTP_FROM') or user
    use_tls = os.getenv('SMTP_TLS', 'true').lower() in ('1', 'true', 'yes', 'on')
    debug = os.getenv('SMTP_DEBUG', 'false').lower() in ('1', 'true', 'yes', 'on')

    if not all([host, port, user, password]):
        return False, 'Configuração SMTP ausente. Defina SMTP_HOST/PORT/USER/PASSWORD no .env'

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    if text_body:
        msg.set_content(text_body)
    else:
        # conteúdo texto simples mínimo
        msg.set_content('')

    # Alternativa HTML
    if html_body:
        msg.add_alternative(html_body, subtype='html')

    try:
        context = _build_ssl_context()
        if use_tls and port in (25, 587):
            # STARTTLS
            with smtplib.SMTP(host, port, timeout=30) as server:
                if debug:
                    server.set_debuglevel(1)
                    try:
                        safe_from = from_email if from_email else '(none)'
                        print(f"[SMTP DEBUG] Conectando via STARTTLS -> host={host} port={port} user={user} from={safe_from}")
                    except Exception:
                        pass
                server.ehlo()
                server.starttls(context=context)
                # Log do certificado do peer após handshake TLS
                try:
                    peer_cert = server.sock.getpeercert()
                    if debug:
                        print(f"[SMTP DEBUG] Peer cert subject: {peer_cert.get('subject')} issuer: {peer_cert.get('issuer')}")
                except Exception as cert_err:
                    if debug:
                        print(f"[SMTP DEBUG] Não foi possível obter certificado do peer: {cert_err}")
                server.login(user, password)
                server.send_message(msg)
        else:
            # SSL (465) ou sem TLS (não recomendado)
            with smtplib.SMTP_SSL(host, port, context=context, timeout=30) as server:
                if debug:
                    server.set_debuglevel(1)
                    try:
                        safe_from = from_email if from_email else '(none)'
                        print(f"[SMTP DEBUG] Conectando via SSL -> host={host} port={port} user={user} from={safe_from}")
                    except Exception:
                        pass
                try:
                    peer_cert = server.sock.getpeercert()
                    if debug:
                        print(f"[SMTP DEBUG] Peer cert subject: {peer_cert.get('subject')} issuer: {peer_cert.get('issuer')}")
                except Exception as cert_err:
                    if debug:
                        print(f"[SMTP DEBUG] Não foi possível obter certificado do peer: {cert_err}")
                server.login(user, password)
                server.send_message(msg)
        return True, None
    except Exception as e:
        if debug:
            print(f"[SMTP ERROR] {e}")
        return False, str(e)
