from flask import Flask
from flask_cors import CORS
from config.database import init_db
from routes.auth_routes import auth_bp
from routes.user_routes import user_bp
from routes.entrada_routes import entrada_bp
from routes.saida_routes import saida_bp
from routes.analise_routes import analise_bp
from routes.investimento_routes import investimento_bp
from routes.smtp_routes import smtp_bp
from routes.recuperacao_senha_routes import recuperacao_bp
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

# Configurações
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

# Inicializar banco de dados
init_db()

# Registrar blueprints (rotas)
app.register_blueprint(auth_bp, url_prefix='/api')
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(entrada_bp, url_prefix='/api')
app.register_blueprint(saida_bp, url_prefix='/api')
app.register_blueprint(analise_bp, url_prefix='/api')
app.register_blueprint(investimento_bp, url_prefix='/api')
app.register_blueprint(recuperacao_bp, url_prefix='/api')
app.register_blueprint(smtp_bp, url_prefix='/api')

@app.route('/', methods=['GET'])
def home():
    """Rota de teste"""
    return {
        'mensagem': 'API GeFi está funcionando! 🚀',
        'versao': '1.0.0',
        'arquitetura': 'MVC',
        'endpoints': {
            'autenticacao': [
                'POST /api/cadastro',
                'POST /api/login',
                'POST /api/recuperar-senha',
                'PUT /api/mudar-senha'
            ],
            'usuario': [
                'GET /api/usuario',
                'POST /api/questionario'
            ],
            'entradas': [
                'POST /api/entrada',
                'GET /api/entradas',
                'PUT /api/entrada/<id>',
                'DELETE /api/entrada/<id>'
            ],
            'saidas': [
                'POST /api/saida',
                'GET /api/saidas',
                'PUT /api/saida/<id>',
                'DELETE /api/saida/<id>'
            ],
            'analises': [
                'GET /api/balanco',
                'GET /api/proximas-saidas',
                'GET /api/categorias-gastos'
            ],
            'investimentos': [
                'GET /api/investimentos'
            ]
        }
    }, 200

if __name__ == '__main__':
    # Evita erro WinError 10038 no Windows ao usar reloader
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)