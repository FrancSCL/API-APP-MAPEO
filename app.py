#!/usr/bin/env python3
"""
Flask Application Factory
"""

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import os

def create_app():
    """Create and configure the Flask application"""
    
    # Create Flask app
    app = Flask(__name__)
    
    # Configure CORS
    CORS(app)
    
    # Load configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-secret-key')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'default-jwt-secret')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False  # Tokens don't expire
    
    # Initialize JWT
    jwt = JWTManager(app)
    
    # Import and register blueprints
    from blueprints.auth import auth_bp
    from blueprints.usuarios import usuarios_bp
    from blueprints.cuarteles import cuarteles_bp
    from blueprints.plantas import plantas_bp
    from blueprints.hileras import hileras_bp
    from blueprints.variedades import variedades_bp
    from blueprints.especies import especies_bp
    from blueprints.registromapeo import registromapeo_bp
    from blueprints.registros import registros_bp
    from blueprints.tipoplanta import tipoplanta_bp
    from blueprints.estadocatastro import estadocatastro_bp
    from blueprints.opciones import opciones_bp
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(usuarios_bp, url_prefix='/api/usuarios')
    app.register_blueprint(cuarteles_bp, url_prefix='/api/cuarteles')
    app.register_blueprint(plantas_bp, url_prefix='/api/plantas')
    app.register_blueprint(hileras_bp, url_prefix='/api/hileras')
    app.register_blueprint(variedades_bp, url_prefix='/api/variedades')
    app.register_blueprint(especies_bp, url_prefix='/api/especies')
    app.register_blueprint(registromapeo_bp, url_prefix='/api/registromapeo')
    app.register_blueprint(registros_bp, url_prefix='/api/registros')
    app.register_blueprint(tipoplanta_bp, url_prefix='/api/tipoplanta')
    app.register_blueprint(estadocatastro_bp, url_prefix='/api/estadocatastro')
    app.register_blueprint(opciones_bp, url_prefix='/api/opciones')
    
    # Root route
    @app.route('/')
    def root():
        return {
            "message": "API de Mapeo Agrícola",
            "version": "2.1",
            "status": "active",
            "endpoints": {
                "auth": "/api/auth",
                "usuarios": "/api/usuarios",
                "cuarteles": "/api/cuarteles",
                "plantas": "/api/plantas",
                "hileras": "/api/hileras",
                "variedades": "/api/variedades",
                "especies": "/api/especies",
                "registromapeo": "/api/registromapeo",
                "registros": "/api/registros",
                "tipoplanta": "/api/tipoplanta",
                "estadocatastro": "/api/estadocatastro",
                "opciones": "/api/opciones"
            }
        }
    
    # Health check route
    @app.route('/health')
    def health():
        return {"status": "healthy", "version": "2.1"}
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=int(os.getenv('PORT', 8080)))
