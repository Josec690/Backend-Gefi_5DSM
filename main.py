from flask import Flask
from flask_cors import CORS
from app.database.connection import init_db, close_db, get_db
from app.database.indexes import create_indexes
from app.views.auth_routes import auth_bp
from app.views.financial_routes import financial_bp
from app.views.market_routes import market_bp  # ADICIONE ESTA LINHA
from app.config import config
import os

def create_app(config_name=None):
    """Factory para criar aplicação Flask"""
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Inicializar banco de dados
    with app.app_context():
        init_db()
        db = get_db()
        create_indexes(db)
    
    # CORS
    CORS(app, resources={
        r"/*": {
            "origins": "*",
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # Registrar blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(financial_bp)
    app.register_blueprint(market_bp)  # ADICIONE ESTA LINHA
    
    # Handlers
    @app.teardown_appcontext
    def teardown_db(exception=None):
        db = get_db()
        if db:
            pass  # MongoDB fecha automaticamente
    
    @app.route('/')
    def root():
        """Endpoint raiz"""
        return {
            "message": "GeFi Backend API - Flask",
            "version": "1.0.0",
            "status": "running",
            "docs": "/docs"
        }
    
    @app.route('/health')
    def health():
        """Health check"""
        return {"status": "healthy"}
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=8000, debug=True)