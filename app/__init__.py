from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import config
import os

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app(config_name=None):
    """Application factory pattern"""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    CORS(app)
    
    # Setup logging
    from app.middleware.logging_middleware import setup_logging, log_request, log_response
    setup_logging(app)
    app.before_request(log_request)
    app.after_request(log_response)
    
    # Register error handlers
    from app.utils.error_handlers import register_error_handlers
    register_error_handlers(app)
    
    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.admin import admin_bp
    from app.routes.tech_writer import writer_bp
    from app.routes.user import user_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(writer_bp, url_prefix='/api/writer')
    app.register_blueprint(user_bp, url_prefix='/api')
    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        return {'status': 'healthy', 'version': '1.0.0'}, 200
    
    # API info endpoint
    @app.route('/api')
    def api_info():
        return {
            'name': 'Moringa Daily.dev API',
            'version': '1.0.0',
            'description': 'Backend API for Moringa School content platform',
            'endpoints': {
                'auth': '/api/auth',
                'admin': '/api/admin',
                'writer': '/api/writer',
                'content': '/api/content',
                'health': '/health'
            }
        }, 200
    
    return app